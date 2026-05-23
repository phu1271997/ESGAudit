# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class Contract(gl.Contract):
    """
    ESGAudit Core Intelligent Contract on GenLayer.
    Automates ESG Report audits and detects greenwashing using Web scraping and LLM consensus.
    """
    audit_counter: u256
    challenge_counter: u256
    audit_fees_collected: u256
    challenger_bounty_pool: u256
    
    audits: TreeMap[u256, str]                   # audit_id -> JSON string
    company_current_badge: TreeMap[str, str]      # company_name -> JSON string
    company_audit_history: TreeMap[str, str]      # company_name -> JSON array of audit_ids
    company_address_to_name: TreeMap[Address, str]# Address -> company_name
    audit_subscription: TreeMap[str, u256]        # company_name -> expiry timestamp
    challenges: TreeMap[u256, str]               # challenge_id -> JSON string
    
    audit_ids: DynArray[u256]
    verified_companies: DynArray[str]            # list of companies with GREEN badge active

    def __init__(self):
        # Rule #2: DO NOT reassign TreeMap or DynArray in __init__
        self.audit_counter = u256(0)
        self.challenge_counter = u256(0)
        self.audit_fees_collected = u256(0)
        self.challenger_bounty_pool = u256(0)

    @gl.public.write
    def register_company(self, company_name: str) -> None:
        """
        Registers a company name for the message sender.
        """
        sender = gl.message.sender_address
        # Check if address already registered
        if sender in self.company_address_to_name:
            return
        self.company_address_to_name[sender] = company_name

    @gl.public.write
    def submit_audit(self, company_name: str, report_url: str, evidence_urls: str, audit_scope: str, fee_paid: int) -> u256:
        """
        Submits a new audit request.
        `evidence_urls` should be a JSON array string containing URLs of supporting documents.
        """
        audit_id = self.audit_counter
        self.audit_counter += u256(1)
        
        # Construct the initial audit record
        audit_record = {
            "id": int(audit_id),
            "company_name": company_name,
            "company_address": str(gl.message.sender_address),
            "report_url": report_url,
            "evidence_urls": evidence_urls,
            "audit_scope": audit_scope,
            "fee_paid": fee_paid,
            "status": "PENDING",
            "ai_verdict_json": "",
            "badge_type": "NONE",
            "expiry_timestamp": 0,
            "created_at": 1774300000 # Mock unix timestamp for 2026
        }
        
        self.audits[audit_id] = json.dumps(audit_record)
        self.audit_ids.append(audit_id)
        self.audit_fees_collected += u256(fee_paid)
        
        # Append to audit history of the company
        history_list = []
        if company_name in self.company_audit_history:
            history_list = json.loads(self.company_audit_history[company_name])
        history_list.append(int(audit_id))
        self.company_audit_history[company_name] = json.dumps(history_list)
        
        return audit_id

    @gl.public.write
    def trigger_ai_audit(self, audit_id: u256) -> str:
        """
        Triggers the AI audit pipeline for a pending audit request.
        Uses GenLayer's non-deterministic web scraper and LLM prompt execution.
        """
        # 1. Fetch audit details from storage
        if audit_id not in self.audits:
            return "ERROR: Audit ID not found"
            
        audit_str = self.audits[audit_id]
        audit_data = json.loads(audit_str)
        
        if audit_data["status"] != "PENDING":
            return "ERROR: Audit is not pending"
            
        company_name = audit_data["company_name"]
        report_url = audit_data["report_url"]
        evidence_urls_str = audit_data["evidence_urls"]
        audit_scope = audit_data["audit_scope"]
        
        # Parse evidence URLs list
        try:
            evidence_urls_list = json.loads(evidence_urls_str)
        except:
            evidence_urls_list = []

        # 2. Define the leader function that performs internet requests and LLM call
        def leader_fn() -> str:
            # Fetch primary report content
            primary_content = ""
            try:
                primary_content = gl.nondet.web.render(report_url, mode="text")
                primary_content = primary_content[:15000] # Limit content length
            except Exception as e:
                primary_content = f"Failed to fetch primary report: {str(e)}"

            # Fetch supporting evidence contents
            evidence_contents = []
            for i, url in enumerate(evidence_urls_list):
                if i >= 4: # Limit to max 4 additional sources to prevent context overflow
                    break
                try:
                    content = gl.nondet.web.render(url, mode="text")
                    evidence_contents.append({
                        "url": url,
                        "content": content[:8000] # Limit content length
                    })
                except Exception as e:
                    evidence_contents.append({
                        "url": url,
                        "content": f"Failed to fetch content: {str(e)}"
                    })

            # Format evidence sections for prompt
            sources_prompt_str = ""
            for idx, item in enumerate(evidence_contents):
                sources_prompt_str += f"\nSource {idx + 1} - ({item['url']}):\n{item['content']}\n"

            # Construct the comprehensive prompt
            prompt = f"""You are a senior ESG auditor with 20 years of experience at KPMG and Deloitte.
You specialize in detecting greenwashing using GRI, SASB, and TCFD frameworks.

COMPANY: {company_name}
AUDIT SCOPE: {audit_scope}

PRIMARY ESG REPORT (from company official source):
{primary_content}

SUPPORTING EVIDENCE FROM WEB:
{sources_prompt_str}

Your task: produce a RIGOROUS ESG audit detecting greenwashing.

GREENWASHING DETECTION CHECKLIST (be skeptical, look for):
1. **Vague language**: "committed to sustainability" without specific targets/dates.
2. **Missing Scope 3 emissions** (most companies hide this — biggest red flag).
3. **No third-party assurance** (PwC, KPMG sign-off?).
4. **Unverified carbon offsets** (offsets from suspect registries?).
5. **Contradictions with news** (claims green while NGO reports oil spills?).
6. **Cherry-picking metrics** (showing 1 good number, hiding 10 bad ones?).
7. **No baseline year disclosed** (can't measure progress without baseline).
8. **Symbolic gestures** (planting trees != reducing emissions).
9. **Future commitments without interim milestones** ("net zero by 2050" with no 2030 target).
10. **Inconsistency between subsidiaries** (parent green, subsidiary destroying forests).

EVALUATION RUBRIC (per pillar):
- **Environmental**: Emissions (scope 1/2/3), water, waste, biodiversity, energy mix.
- **Social**: Labor practices, supply chain ethics, community impact, diversity.
- **Governance**: Board diversity, executive pay, anti-corruption, transparency.

Return ONLY valid JSON in this exact schema:
{{
  "company_name": "{company_name}",
  "audit_scope": "{audit_scope}",
  "overall_score": 0,
  "verdict": "GREEN_VERIFIED | YELLOW_CONDITIONAL | RED_GREENWASHING",
  "pillar_scores": {{
    "environmental": 0,
    "social": 0,
    "governance": 0
  }},
  "claims_verified": [
    {{"claim": "quote from company report", "evidence": "finding from source", "verified": true}}
  ],
  "greenwashing_indicators": [
    {{"type": "VAGUE_LANGUAGE | MISSING_SCOPE3 | NO_TARGETS | UNVERIFIED_OFFSETS | NGO_COMPLAINT | CONTRADICTION | NO_ASSURANCE", "detail": "explanation"}}
  ],
  "red_flags": [
    {{"severity": "LOW | MEDIUM | HIGH | CRITICAL", "issue": "description"}}
  ],
  "data_quality": {{
    "scope1_disclosed": true,
    "scope2_disclosed": true,
    "scope3_disclosed": true,
    "third_party_assured": true,
    "follows_gri": true,
    "follows_tcfd": true
  }},
  "improvement_recommendations": ["recommendation"],
  "evidence_sources_used": ["urls"],
  "confidence_score": 0,
  "auditor_reasoning": "5-7 sentence detailed reasoning"
}}

Verdict thresholds:
- GREEN_VERIFIED (80-100): Strong evidence, follows standards, no major red flags.
- YELLOW_CONDITIONAL (50-79): Some issues — must address flagged items before next audit.
- RED_GREENWASHING (0-49): Significant greenwashing detected — public warning issued.

Be skeptical. Big4-level rigor. Investors depend on your accuracy.
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        # 3. Define the validator function to ensure response matches expectations
        def validator_fn(leader_result) -> bool:
            try:
                if not isinstance(leader_result, gl.vm.Return):
                    return False
                val = leader_result.value
                data = json.loads(val)
                # Check for crucial keys in output
                required_fields = ["company_name", "overall_score", "verdict", "pillar_scores", "claims_verified", "greenwashing_indicators", "red_flags", "data_quality", "auditor_reasoning"]
                for f in required_fields:
                    if f not in data:
                        return False
                return True
            except:
                return False

        # 4. Execute the non-deterministic code using the leader/validator consensus
        # Rule #7: Must wrap gl.nondet.* inside gl.vm.run_nondet_unsafe
        verdict_json = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        
        # 5. Parse output and update contract state
        verdict_data = json.loads(verdict_json)
        
        overall_score = verdict_data["overall_score"]
        verdict = verdict_data["verdict"]
        
        badge_type = "NONE"
        if verdict == "GREEN_VERIFIED":
            badge_type = "GREEN"
        elif verdict == "YELLOW_CONDITIONAL":
            badge_type = "YELLOW"
        elif verdict == "RED_GREENWASHING":
            badge_type = "RED"
            
        expiry = 1774300000 + (365 * 24 * 3600)  # 1 year validity

        # Update audit record
        audit_data["status"] = "COMPLETED"
        audit_data["ai_verdict_json"] = verdict_json
        audit_data["badge_type"] = badge_type
        audit_data["expiry_timestamp"] = expiry
        
        self.audits[audit_id] = json.dumps(audit_data)

        # Update current badge
        badge_record = {
            "badge_type": badge_type,
            "audit_id": int(audit_id),
            "expiry": expiry,
            "score": overall_score
        }
        self.company_current_badge[company_name] = json.dumps(badge_record)

        # Update verified companies registry
        if badge_type == "GREEN":
            # Add to green registry if not present
            found = False
            for i in range(len(self.verified_companies)):
                if self.verified_companies[i] == company_name:
                    found = True
                    break
            if not found:
                self.verified_companies.append(company_name)
        else:
            # Remove from green registry if present
            temp_list = []
            for i in range(len(self.verified_companies)):
                if self.verified_companies[i] != company_name:
                    temp_list.append(self.verified_companies[i])
            
            # Rebuild DynArray
            while len(self.verified_companies) > 0:
                self.verified_companies.pop()
            for name in temp_list:
                self.verified_companies.append(name)

        return verdict_json

    @gl.public.write
    def submit_challenge(self, audit_id: u256, evidence_url: str, reason: str) -> u256:
        """
        Allows anyone (whistleblowers) to submit counter-evidence against a verified company.
        """
        challenge_id = self.challenge_counter
        self.challenge_counter += u256(1)
        
        challenge_record = {
            "id": int(challenge_id),
            "audit_id": int(audit_id),
            "challenger": str(gl.message.sender_address),
            "evidence_url": evidence_url,
            "reason": reason,
            "status": "PENDING"
        }
        
        self.challenges[challenge_id] = json.dumps(challenge_record)
        return challenge_id

    @gl.public.write
    def process_challenge(self, challenge_id: u256) -> str:
        """
        Re-audits a company based on whistleblower evidence.
        If challenge is valid, update company badge and award bounty.
        """
        if challenge_id not in self.challenges:
            return "ERROR: Challenge ID not found"
            
        challenge_str = self.challenges[challenge_id]
        challenge_data = json.loads(challenge_str)
        
        if challenge_data["status"] != "PENDING":
            return "ERROR: Challenge is already processed"
            
        audit_id = u256(challenge_data["audit_id"])
        evidence_url = challenge_data["evidence_url"]
        reason = challenge_data["reason"]
        
        if audit_id not in self.audits:
            return "ERROR: Linked audit ID not found"
            
        audit_str = self.audits[audit_id]
        audit_data = json.loads(audit_str)
        
        company_name = audit_data["company_name"]
        primary_report_url = audit_data["report_url"]
        
        # AI re-audit logic wrapped in run_nondet_unsafe
        def leader_fn() -> str:
            # Read primary report
            primary_content = ""
            try:
                primary_content = gl.nondet.web.render(primary_report_url, mode="text")
                primary_content = primary_content[:10000]
            except Exception as e:
                primary_content = f"Failed to fetch report: {str(e)}"
                
            # Read challenger evidence
            challenge_content = ""
            try:
                challenge_content = gl.nondet.web.render(evidence_url, mode="text")
                challenge_content = challenge_content[:8000]
            except Exception as e:
                challenge_content = f"Failed to fetch whistleblower evidence: {str(e)}"
                
            prompt = f"""You are a senior ESG auditor reviewing a CHALLENGE submitted by a whistleblower.
The whistleblower claims that the company "{company_name}" is engaging in greenwashing, contrary to their ESG reports.

COMPANY: {company_name}
PRIMARY ESG REPORT: {primary_content}

WHISTLEBLOWER REASON FOR CHALLENGE:
{reason}

WHISTLEBLOWER EVIDENCE (from {evidence_url}):
{challenge_content}

Re-evaluate the ESG report in light of this whistleblower challenge. Be highly skeptical.
Does this challenge provide verified proof of greenwashing or contradiction?
If yes, drastically decrease the overall_score and change verdict to RED_GREENWASHING or YELLOW_CONDITIONAL.

Return ONLY valid JSON in this exact schema:
{{
  "challenge_valid": true,
  "explanation": "why the challenge is valid or invalid",
  "company_name": "{company_name}",
  "overall_score": 0,
  "verdict": "GREEN_VERIFIED | YELLOW_CONDITIONAL | RED_GREENWASHING",
  "pillar_scores": {{
    "environmental": 0,
    "social": 0,
    "governance": 0
  }},
  "claims_verified": [
    {{"claim": "quote", "evidence": "finding", "verified": false}}
  ],
  "greenwashing_indicators": [
    {{"type": "CONTRADICTION", "detail": "detail"}}
  ],
  "red_flags": [
    {{"severity": "CRITICAL", "issue": "detail"}}
  ],
  "data_quality": {{
    "scope1_disclosed": true,
    "scope2_disclosed": true,
    "scope3_disclosed": true,
    "third_party_assured": true,
    "follows_gri": true,
    "follows_tcfd": true
  }},
  "improvement_recommendations": ["recommendation"],
  "evidence_sources_used": ["{evidence_url}"],
  "confidence_score": 0,
  "auditor_reasoning": "5-7 sentences explanation of the challenge verdict"
}}
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leader_result) -> bool:
            try:
                if not isinstance(leader_result, gl.vm.Return):
                    return False
                val = leader_result.value
                data = json.loads(val)
                required_fields = ["challenge_valid", "explanation", "overall_score", "verdict", "pillar_scores", "auditor_reasoning"]
                for f in required_fields:
                    if f not in data:
                        return False
                return True
            except:
                return False

        verdict_json = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        verdict_data = json.loads(verdict_json)
        
        is_valid = verdict_data["challenge_valid"]
        new_score = verdict_data["overall_score"]
        new_verdict = verdict_data["verdict"]
        
        # Update challenge status
        challenge_data["status"] = "VALID" if is_valid else "INVALID"
        self.challenges[challenge_id] = json.dumps(challenge_data)
        
        # If challenge is valid, demote company and distribute bounty if pool has funds
        if is_valid:
            badge_type = "NONE"
            if new_verdict == "GREEN_VERIFIED":
                badge_type = "GREEN"
            elif new_verdict == "YELLOW_CONDITIONAL":
                badge_type = "YELLOW"
            elif new_verdict == "RED_GREENWASHING":
                badge_type = "RED"
                
            expiry = 1774300000 + (365 * 24 * 3600)

            # Update original audit record
            audit_data["badge_type"] = badge_type
            audit_data["ai_verdict_json"] = verdict_json
            self.audits[audit_id] = json.dumps(audit_data)

            # Update current badge
            badge_record = {
                "badge_type": badge_type,
                "audit_id": int(audit_id),
                "expiry": expiry,
                "score": new_score
            }
            self.company_current_badge[company_name] = json.dumps(badge_record)

            # Rebuild verified companies list if company no longer green
            if badge_type != "GREEN":
                temp_list = []
                for i in range(len(self.verified_companies)):
                    if self.verified_companies[i] != company_name:
                        temp_list.append(self.verified_companies[i])
                
                while len(self.verified_companies) > 0:
                    self.verified_companies.pop()
                for name in temp_list:
                    self.verified_companies.append(name)
                    
            # Simulate bounty distribution from challenger bounty pool
            # ...

        return verdict_json

    @gl.public.write
    def subscribe_continuous_monitoring(self, company_name: str, months: int) -> None:
        """
        Subscribes a company to continuous quarterly monitoring.
        """
        expiry = 1774300000 + (months * 30 * 24 * 3600)
        self.audit_subscription[company_name] = u256(expiry)
        
        # Lock subset as whistleblower bounty pool (mock implementation)
        self.challenger_bounty_pool += u256(100) # Mock 100 USDC added to bounty pool

    @gl.public.write
    def trigger_quarterly_recheck(self, company_name: str) -> str:
        """
        Triggers a quarterly automatic recheck for subscribed companies.
        Reads news and recent web mentions to verify if any major scandals have occurred.
        """
        if company_name not in self.audit_subscription:
            return "ERROR: Company not subscribed to monitoring"
            
        # Get latest active badge
        if company_name not in self.company_current_badge:
            return "ERROR: No active audit badge found for company"
            
        badge_data = json.loads(self.company_current_badge[company_name])
        audit_id = u256(badge_data["audit_id"])
        
        audit_str = self.audits[audit_id]
        audit_data = json.loads(audit_str)
        report_url = audit_data["report_url"]
        
        # We search news databases using web render
        def leader_fn() -> str:
            # Let's search recent sustainability news about the company
            news_url = f"https://www.google.com/search?q={company_name}+ESG+scandal+greenwashing&tbm=nws"
            news_content = ""
            try:
                news_content = gl.nondet.web.render(news_url, mode="text")
                news_content = news_content[:12000]
            except Exception as e:
                news_content = f"Failed to fetch news: {str(e)}"
                
            prompt = f"""You are a senior ESG auditor performing a quarterly continuous monitoring check.
Company Name: {company_name}

LATEST SEARCH RESULTS FOR ESG SCANDALS/GREENWASHING:
{news_content}

Does this company have any new critical ESG incidents, supply chain scandals, environmental spills, or regulatory fines mentioned in the news?
If YES, you should flag these.
If NO, verify they remain compliant.

Return ONLY valid JSON in this exact schema:
{{
  "company_name": "{company_name}",
  "has_new_scandals": true,
  "scandals_detected": [
    {{"severity": "CRITICAL | HIGH | MEDIUM | LOW", "source": "News headline", "detail": "explanation"}}
  ],
  "overall_score_adjustment": -10, // negative integer or 0
  "verdict": "GREEN_VERIFIED | YELLOW_CONDITIONAL | RED_GREENWASHING",
  "reasoning": "5-7 sentences detailed explanation"
}}
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leader_result) -> bool:
            try:
                if not isinstance(leader_result, gl.vm.Return):
                    return False
                val = leader_result.value
                data = json.loads(val)
                required_fields = ["company_name", "has_new_scandals", "scandals_detected", "overall_score_adjustment", "verdict", "reasoning"]
                for f in required_fields:
                    if f not in data:
                        return False
                return True
            except:
                return False

        recheck_json = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        recheck_data = json.loads(recheck_json)
        
        has_new_scandals = recheck_data["has_new_scandals"]
        score_adj = recheck_data["overall_score_adjustment"]
        new_verdict = recheck_data["verdict"]
        
        if has_new_scandals and score_adj != 0:
            badge_data["score"] = max(0, badge_data["score"] + score_adj)
            
            badge_type = "NONE"
            if new_verdict == "GREEN_VERIFIED":
                badge_type = "GREEN"
            elif new_verdict == "YELLOW_CONDITIONAL":
                badge_type = "YELLOW"
            elif new_verdict == "RED_GREENWASHING":
                badge_type = "RED"
                
            badge_data["badge_type"] = badge_type
            self.company_current_badge[company_name] = json.dumps(badge_data)
            
            # Update verified companies array
            if badge_type != "GREEN":
                temp_list = []
                for i in range(len(self.verified_companies)):
                    if self.verified_companies[i] != company_name:
                        temp_list.append(self.verified_companies[i])
                
                while len(self.verified_companies) > 0:
                    self.verified_companies.pop()
                for name in temp_list:
                    self.verified_companies.append(name)
                    
        return recheck_json

    @gl.public.view
    def get_audit(self, audit_id: u256) -> str:
        """
        Returns JSON representation of the audit details.
        """
        if audit_id in self.audits:
            return self.audits[audit_id]
        return ""

    @gl.public.view
    def get_company_badge(self, company_name: str) -> str:
        """
        Returns JSON representation of the company's active badge.
        """
        if company_name in self.company_current_badge:
            return self.company_current_badge[company_name]
        return ""

    @gl.public.view
    def get_company_history(self, company_name: str) -> str:
        """
        Returns JSON array string of audit IDs for the company.
        """
        if company_name in self.company_audit_history:
            return self.company_audit_history[company_name]
        return "[]"

    @gl.public.view
    def list_green_verified_companies(self) -> DynArray[str]:
        """
        Returns a list of all green verified companies.
        """
        return self.verified_companies

    @gl.public.view
    def list_audits_by_scope(self, scope: str) -> DynArray[u256]:
        """
        Filters and returns audit IDs matching the requested scope.
        """
        # Re-build matching list
        matching = DynArray[u256]()
        for i in range(len(self.audit_ids)):
            audit_id = self.audit_ids[i]
            audit_data = json.loads(self.audits[audit_id])
            if audit_data["audit_scope"] == scope:
                matching.append(audit_id)
        return matching

    @gl.public.view
    def is_badge_active(self, company_name: str) -> bool:
        """
        Checks if the company's badge is active and not expired.
        """
        if company_name not in self.company_current_badge:
            return False
        badge_data = json.loads(self.company_current_badge[company_name])
        # Current mock timestamp is 1774300000. In real life, compare against gl.block.timestamp.
        # Let's say expiry must be > current time (mocking 1774300000)
        return badge_data["expiry"] > 1774300000

    @gl.public.view
    def get_challenge(self, challenge_id: u256) -> str:
        """
        Returns JSON representation of the challenge details.
        """
        if challenge_id in self.challenges:
            return self.challenges[challenge_id]
        return ""
