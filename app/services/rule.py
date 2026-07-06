from __future__ import annotations
import logging, random, re
from app.models.enums import RuleType
from app.models.rule import Rule
from app.repositories.rule import RuleRepository
from app.utils.exceptions import NotFoundError

logger = logging.getLogger(__name__)

class RuleService:
    def __init__(self, repo: RuleRepository | None = None) -> None: self.repo = repo
    @staticmethod
    def _match_rule(rule: Rule, text: str) -> bool:
        if not text or not rule.is_active: return False
        text_cmp = text if rule.case_sensitive else text.lower()
        pattern = rule.pattern if rule.case_sensitive else rule.pattern.lower()
        try:
            if rule.rule_type == RuleType.EXACT: return text_cmp == pattern
            if rule.rule_type == RuleType.CONTAINS: return pattern in text_cmp
            if rule.rule_type == RuleType.STARTS_WITH: return text_cmp.startswith(pattern)
            if rule.rule_type == RuleType.ENDS_WITH: return text_cmp.endswith(pattern)
            if rule.rule_type == RuleType.REGEX: return re.search(rule.pattern, text, flags=0 if rule.case_sensitive else re.IGNORECASE) is not None
        except re.error:
            logger.warning("Invalid regex in rule id=%s", rule.id); return False
        return False
    def find_match(self, rules: list[Rule], text: str) -> Rule | None:
        for r in rules:
            if self._match_rule(r, text): return r
        return None
    def pick_reply(self, rule: Rule) -> dict:
        if rule.random_replies:
            chosen = random.choice(rule.random_replies)
            return {"type": chosen.get("type", rule.reply_type.name), "text": chosen.get("text"), "file_id": chosen.get("file_id")}
        return {"type": rule.reply_type.name, "text": rule.reply_text, "file_id": rule.reply_file_id}
    async def create(self, user_id: int, data) -> Rule:
        rule = Rule(user_id=user_id, **data.model_dump())
        return await self.repo.add(rule)
    async def update(self, rule_id: int, data) -> Rule:
        r = await self.repo.get(rule_id)
        if not r: raise NotFoundError("Rule not found")
        for k, v in data.model_dump(exclude_unset=True).items(): setattr(r, k, v)
        return r
    async def delete(self, rule_id: int) -> bool: return await self.repo.delete(rule_id)
    async def list_for(self, user_id: int) -> list[Rule]: return await self.repo.list_for_user(user_id)
    async def bump_match(self, rule_id: int) -> None:
        r = await self.repo.get(rule_id)
        if r: r.match_count += 1
