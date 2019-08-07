# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_unit_decl`
Contains the definition of the class that represents the lexing rule
to tokenize a declaration of a unit (from '[' to ']').
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import \
    CASE_GEN_SYM, UNIT_END_SYM, extract_identifier

from chatette.refactor_parsing.lexing.rule_unit_start import RuleUnitStart
from chatette.refactor_parsing.lexing.rule_arg_decl import RuleArgDecl
from chatette.refactor_parsing.lexing.rule_variation import RuleVariation


class RuleUnitDecl(LexingRule):
    def _apply_strategy(self):
        if not self._try_to_match_rule(RuleUnitStart):
            return False
        
        if self._text.startswith(CASE_GEN_SYM, self._next_index):
            self._tokens.append(TerminalType.casegen_marker, CASE_GEN_SYM)
            self._next_index += 1
        
        identifier = extract_identifier(self._text, self._next_index)
        if identifier is not None:
            self._tokens.append(
                LexicalToken(TerminalType.unit_identifier, identifier)
            )
            self._next_index += len(identifier)
        
        if not self._match_any_order([None, RuleArgDecl, RuleVariation]):
            return False
        
        if not self._text.startswith(UNIT_END_SYM, self._next_index):
            self.error_msg = \
                "Invalid token. Expected the end of the unit declaration " + \
                "there (using symbol '" + UNIT_END_SYM + "')."
            return False
        # TODO maybe making a function for this would be useful
        if self._tokens[0].type == TerminalType.alias_decl_start:
            unit_end_type = TerminalType.alias_decl_end
        elif self._tokens[0].type == TerminalType.slot_decl_start:
            unit_end_type = TerminalType.slot_decl_end
        elif self._tokens[0].type == TerminalType.intent_decl_start:
            unit_end_type = TerminalType.intent_decl_end
        else:  # Should never happen
            raise ValueError(
                "An unexpected error happened during parsing: tried to " + \
                "parse the end of a unit but couldn't find its start in " + \
                "the previously parsed data.\nData was: " + str(self._tokens)
            )
        self._tokens.append(LexicalToken(unit_end_type, UNIT_END_SYM))
        self._next_index += 1
        return True
        