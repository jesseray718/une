#!/usr/bin/env python3
"""
openroot_scripture_absorber.py
"Sweep the deep for wisdom" - Information absorption module
Principle: Catch and Store Energy (PM-02)
"""

import json
import os
import hashlib
import time
from pathlib import Path

UNE_ROOT = Path(os.environ.get('HOME', '/data/data/com.termux/files/home')) / "une"
SCRIPTURE_DIR = UNE_ROOT / "scripture"
SCRIPTURE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# SCRIPTURE CORPUS - Foundation Layer Expansion
# Translation: LSB (Legacy Standard Bible) + NASB cross-ref
# License: Scripture is OPEN. No extraction permitted.
# ============================================================

SCRIPTURE_CORPUS = {
    "meta": {
        "version": "2.0",
        "created": "2026-07-22",
        "translations": ["LSB (Legacy Standard Bible)", "NASB (New American Standard Bible)"],
        "license": "OPEN - No extraction, no gatekeeping, no paywall",
        "principle": "Every word that proceeds from the mouth of YAHWEH",
        "source": "github.com/jesseray718/openroot"
    },
    
    "red_letter_yeshua": {
        # Matthew
        "MT-03-15": {
            "lsb": "Permit it at this time; for in this way it is fitting for us to fulfill all righteousness.",
            "ref": "Matthew 3:15",
            "context": "At baptism, permitting John to baptize Him",
            "op": "alignment_before_action. align_with_divine_pattern_first_then_execute.",
            "tags": ["righteousness", "alignment", "beginning"]
        },
        "MT-04-04": {
            "lsb": "It is written, MAN SHALL NOT LIVE ON BREAD ALONE, BUT ON EVERY WORD THAT PROCEEDS OUT OF THE MOUTH OF GOD.",
            "ref": "Matthew 4:4",
            "context": "Temptation in wilderness - responding to hunger",
            "op": "input_not_only_physical. spiritual_input_required. every_word_matters.",
            "tags": ["input", "sustenance", "temptation"]
        },
        "MT-04-7": {
            "lsb": "On the other hand, it is written, YOU SHALL NOT PUT THE LORD YOUR GOD TO THE TEST.",
            "ref": "Matthew 4:7",
            "context": "Refusing to jump from temple",
            "op": "do_not_test_system_boundaries_maliciously. respect_limits.",
            "tags": ["testing", "limits", "temptation"]
        },
        "MT-04-10": {
            "lsb": "Go, Satan! For it is written, YOU SHALL WORSHIP THE LORD YOUR GOD, AND SERVE HIM ONLY.",
            "ref": "Matthew 4:10",
            "context": "Final temptation - refusing worldly power",
            "op": "reject_extraction_offer. worship_source_only. serve_not_exploit.",
            "tags": ["worship", "temptation", "power", "extraction"]
        },
        "MT-04-17": {
            "lsb": "Repent, for the kingdom of heaven is at hand.",
            "ref": "Matthew 4:17",
            "context": "Beginning of ministry",
            "op": "change_direction_when_pattern_detected. kingdom_pattern_available_now.",
            "tags": ["repentance", "kingdom", "beginning"]
        },
        "MT-04-19": {
            "lsb": "Follow Me, and I will make you fishers of men.",
            "ref": "Matthew 4:19",
            "context": "Calling first disciples",
            "op": "follow_pattern_of_master. transform_profession_into_purpose.",
            "tags": ["calling", "transformation", "discipleship"]
        },
        "MT-05-3": {
            "lsb": "Blessed are the poor in spirit, for theirs is the kingdom of heaven.",
            "ref": "Matthew 5:3",
            "context": "Sermon on Mount - Beatitudes",
            "op": "emptiness_is_precondition_for_filling. least_capable_receives_first.",
            "tags": ["beatitude", "humility", "kingdom"]
        },
        "MT-05-4": {
            "lsb": "Blessed are those who mourn, for they shall be comforted.",
            "ref": "Matthew 5:4",
            "op": "acknowledge_loss_openly. comfort_follows_grief_not_denial.",
            "tags": ["beatitude", "grief", "comfort"]
        },
        "MT-05-5": {
            "lsb": "Blessed are the gentle, for they shall inherit the earth.",
            "ref": "Matthew 5:5",
            "op": "gentle_force_persists. not_aggressive_dominance. land_given_not_taken.",
            "tags": ["beatitude", "meekness", "inheritance"]
        },
        "MT-05-6": {
            "lsb": "Blessed are those who hunger and thirst for righteousness, for they shall be satisfied.",
            "ref": "Matthew 5:6",
            "op": "active_desire_for_justice. satisfaction_guaranteed. system_must_deliver.",
            "tags": ["beatitude", "justice", "satisfaction"]
        },
        "MT-05-7": {
            "lsb": "Blessed are the merciful, for they shall receive mercy.",
            "ref": "Matthew 5:7",
            "op": "mercy_circulates. give_mercy_receive_mercy. feedback_loop.",
            "tags": ["beatitude", "mercy", "reciprocity"]
        },
        "MT-05-8": {
            "lsb": "Blessed are the pure in heart, for they shall see God.",
            "ref": "Matthew 5:8",
            "op": "no_hidden_motive. transparent_intent_enables_perception_of_source.",
            "tags": ["beatitude", "purity", "vision"]
        },
        "MT-05-9": {
            "lsb": "Blessed are the peacemakers, for they shall be called sons of God.",
            "ref": "Matthew 5:9",
            "op": "build_systems_that_reduce_conflict. identity_derived_from_peace_work.",
            "tags": ["beatitude", "peace", "identity"]
        },
        "MT-05-10": {
            "lsb": "Blessed are those who have been persecuted for the sake of righteousness, for theirs is the kingdom of heaven.",
            "ref": "Matthew 5:10",
            "op": "standing_for_justice_costs_something. cost_proves_authenticity.",
            "tags": ["beatitude", "persecution", "justice"]
        },
        "MT-05-13": {
            "lsb": "You are the salt of the earth; but if the salt has become tasteless, how will it be made salty again? It is no longer good for anything, except to be thrown out and trampled under foot by men.",
            "ref": "Matthew 5:13",
            "op": "preserve_value. if_you_lose_function_you_become_noise. stay_sharp.",
            "tags": ["identity", "preservation", "utility"]
        },
        "MT-05-14": {
            "lsb": "You are the light of the world. A city set on a hill cannot be hidden.",
            "ref": "Matthew 5:14",
            "op": "visibility_is_not_optional. open_source_not_hidden. illuminate.",
            "tags": ["identity", "light", "visibility", "open"]
        },
        "MT-05-16": {
            "lsb": "Let your light shine before men in such a way that they may see your good works, and glorify your Father who is in heaven.",
            "ref": "Matthew 5:16",
            "op": "visible_work_attributed_to_source. credit_returns_to_most_high.",
            "tags": ["visibility", "works", "attribution"]
        },
        "MT-05-19": {
            "lsb": "Whoever then annuls one of the least of these commandments, and teaches others to do the same, shall be called least in the kingdom of heaven; but whoever keeps and teaches them, he shall be called great in the kingdom of heaven.",
            "ref": "Matthew 5:19",
            "op": "small_details_matter. no_commandment_discarded. smallest_valid_maintained.",
            "tags": ["commandments", "details", "greatness"]
        },
        "MT-05-37": {
            "lsb": "But let your statement be, Yes, yes or No, no; anything beyond these is of evil.",
            "ref": "Matthew 5:37",
            "op": "binary_truth. no_complexity_added_to_simple_statements. say_what_you_mean.",
            "tags": ["truth", "simplicity", "communication"]
        },
        "MT-05-44": {
            "lsb": "But I say to you, love your enemies and pray for those who persecute you.",
            "ref": "Matthew 5:44",
            "op": "invest_in_adversary. no_extraction_even_from_opposition. transform_enemy_via_love.",
            "tags": ["love", "enemies", "transformation"]
        },
        "MT-05-48": {
            "lsb": "Therefore you are to be perfect, as your heavenly Father is perfect.",
            "ref": "Matthew 5:48",
            "op": "target_is_completeness. continuous_improvement_toward_wholeness.",
            "tags": ["perfection", "completeness", "target"]
        },
        "MT-06-9": {
            "lsb": "Pray, then, in this way: Our Father who is in heaven, Hallowed be Your name.",
            "ref": "Matthew 6:9",
            "context": "The Lord's Prayer begins",
            "op": "declare_universal_parentage. all_nodes_equal. source_acknowledged.",
            "tags": ["prayer", "foundation", "parentage"]
        },
        "MT-06-10": {
            "lsb": "Your kingdom come. Your will be done, On earth as it is in heaven.",
            "ref": "Matthew 6:10",
            "op": "bring_divine_pattern_to_material. heaven_efficiency_on_earth.",
            "tags": ["prayer", "kingdom", "efficiency"]
        },
        "MT-06-11": {
            "lsb": "Give us this day our daily bread.",
            "ref": "Matthew 6:11",
            "op": "meet_needs_not_hoard. enough_for_today. no_manufactured_scarcity.",
            "tags": ["prayer", "provision", "daily"]
        },
        "MT-06-12": {
            "lsb": "And forgive us our debts, as we also have forgiven our debtors.",
            "ref": "Matthew 6:12",
            "op": "cancel_extraction_chains. debt_is_control. knowledge_compounds_not_interest.",
            "tags": ["prayer", "forgiveness", "debt"]
        },
        "MT-06-13": {
            "lsb": "And do not lead us into temptation, but deliver us from evil. For Yours is the kingdom and the power and the glory forever. Amen.",
            "ref": "Matthew 6:13",
            "op": "avoid_predatory_path. defend_against_parasite. energy_loops_back_to_source.",
            "tags": ["prayer", "protection", "energy_loop"]
        },
        "MT-06-19": {
            "lsb": "Do not store up for yourselves treasures on earth, where moth and rust destroy, and where thieves break in and steal.",
            "ref": "Matthew 6:19",
            "op": "no_hoarding. earthly_treasure_decays. invest_in_permanent_not_perishable.",
            "tags": ["treasure", "decay", "investment"]
        },
        "MT-06-20": {
            "lsb": "But store up for yourselves treasures in heaven, where neither moth nor rust destroys, and where thieves do not break in or steal.",
            "ref": "Matthew 6:20",
            "op": "invest_in_open_source_knowledge. permanent. cannot_be_stolen_or_corrupted.",
            "tags": ["treasure", "permanent", "investment"]
        },
        "MT-06-21": {
            "lsb": "For where your treasure is, there your heart will be also.",
            "ref": "Matthew 6:21",
            "op": "attention_follows_investment. what_you_fund_is_what_you_love.",
            "tags": ["treasure", "heart", "attention"]
        },
        "MT-06-24": {
            "lsb": "No one can serve two masters; for either he will hate the one and love the other, or he will be devoted to one and despise the other. You cannot serve God and wealth.",
            "ref": "Matthew 6:24",
            "op": "single_source_of_truth. no_dual_allegiance. system_serves_one_purpose.",
            "tags": ["loyalty", "wealth", "singularity"]
        },
        "MT-06-33": {
            "lsb": "But seek first His kingdom and His righteousness, and all these things will be added to you.",
            "ref": "Matthew 6:33",
            "op": "prioritize_divine_pattern. material_follows_correct_order.",
            "tags": ["priority", "kingdom", "provision"]
        },
        "MT-07-7": {
            "lsb": "Ask, and it will be given to you; seek, and you will find; knock, and it will be opened to you.",
            "ref": "Matthew 7:7",
            "op": "active_query_required. system_responds_to_initiative. persistent_request.",
            "tags": ["seeking", "promise", "persistence"]
        },
        "MT-07-12": {
            "lsb": "In everything, therefore, treat people the same way you want them to treat you, for this is the Law and the Prophets.",
            "ref": "Matthew 7:12",
            "context": "The Golden Rule",
            "op": "symmetric_treatment. design_for_reciprocity. test_your_own_system_as_user.",
            "tags": ["golden-rule", "reciprocity", "law"]
        },
        "MT-07-13": {
            "lsb": "Enter through the narrow gate; for the gate is wide and the way is broad that leads to destruction, and there are many who enter through it.",
            "ref": "Matthew 7:13",
            "op": "choose_difficult_efficient_path. easy_path_leads_to_loss. narrow_is_secure.",
            "tags": ["path", "choices", "narrow"]
        },
        "MT-07-16": {
            "lsb": "You will know them by their fruits. Grapes are not gathered from thorn bushes nor figs from thistles, are they?",
            "ref": "Matthew 7:16",
            "op": "evaluate_by_output. pattern_recognition_via_results. tree_known_by_fruit.",
            "tags": ["discernment", "fruits", "evaluation"]
        },
        "MT-07-17": {
            "lsb": "So every good tree bears good fruit, but the bad tree bears bad fruit.",
            "ref": "Matthew 7:17",
            "op": "correlation_between_source_quality_and_output. bad_source_bad_result.",
            "tags": ["discernment", "fruits", "quality"]
        },
        "MT-07-20": {
            "lsb": "So then, you will know them by their fruits.",
            "ref": "Matthew 7:20",
            "op": "output_is_the_proof. claims_irrelevant_without_matching_results.",
            "tags": ["discernment", "proof", "results"]
        },
        "MT-07-24": {
            "lsb": "Therefore everyone who hears these words of Mine and does them, may be compared to a wise man who built his house on the rock.",
            "ref": "Matthew 7:24",
            "op": "hearing_plus_doing_equals_wisdom. application_stabilizes_foundation.",
            "tags": ["wisdom", "foundation", "application"]
        },
        "MT-07-26": {
            "lsb": "Everyone who hears these words of Mine and does not do them, will be like a foolish man who built his house on the sand.",
            "ref": "Matthew 7:26",
            "op": "knowledge_without_application_collapses. theory_without_practice_unstable.",
            "tags": ["foolishness", "instability", "inaction"]
        },
        "MT-10-7": {
            "lsb": "And as you go, preach, saying, The kingdom of heaven is at hand.",
            "ref": "Matthew 10:7",
            "op": "kingdom_available_now. no_waiting. distribute_pattern.",
            "tags": ["kingdom", "mission", "now"]
        },
        "MT-10-8": {
            "lsb": "Heal the sick, raise the dead, cleanse the lepers, cast out demons. Freely you received, freely give.",
            "ref": "Matthew 10:8",
            "op": "received_free_give_free. NO_EXTRACTION. healing_at_zero_cost.",
            "tags": ["healing", "free", "giving"]
        },
        "MT-10-16": {
            "lsb": "Behold, I send you out as sheep in the midst of wolves; so be shrewd as serpents and innocent as doves.",
            "ref": "Matthew 10:16",
            "op": "aware_of_predatory_environment. strategic_but_not_predatory.",
            "tags": ["strategy", "innocence", "awareness"]
        },
        "MT-10-26": {
            "lsb": "Therefore do not fear them, for there is nothing concealed that will not be revealed, or hidden that will not be known.",
            "ref": "Matthew 10:26",
            "op": "radical_transparency_wins. hidden_things_exposed. fear_is_unnecessary.",
            "tags": ["transparency", "fear", "exposure"]
        },
        "MT-10-32": {
            "lsb": "Therefore everyone who confesses Me before men, I will also confess him before My Father who is in heaven.",
            "ref": "Matthew 10:32",
            "op": "public_attribution_of_source. acknowledge_openly.",
            "tags": ["confession", "attribution", "public"]
        },
        "MT-11-15": {
            "lsb": "He who has ears to hear, let him hear.",
            "ref": "Matthew 11:15",
            "op": "capacity_to_receive_varies. only_those_ready_can_process.",
            "tags": ["hearing", "readiness", "capacity"]
        },
        "MT-11-25": {
            "lsb": "I praise You, Father, Lord of heaven and earth, that You have hidden these things from the wise and intelligent and have revealed them to infants.",
            "ref": "Matthew 11:25",
            "op": "complexity_hides_truth. simplicity_reveals_it. design_for_least_sophisticated.",
            "tags": ["simplicity", "hidden", "infants"]
        },
        "MT-11-28": {
            "lsb": "Come to Me, all who are weary and heavy-laden, and I will give you rest.",
            "ref": "Matthew 11:28",
            "op": "system_absorbs_burden. rest_provided_not_earned. carry_each_other.",
            "tags": ["rest", "burden", "invitation"]
        },
        "MT-11-29": {
            "lsb": "Take My yoke upon you and learn from Me, for I am gentle and humble in heart, and YOU WILL FIND REST FOR YOUR SOULS.",
            "ref": "Matthew 11:29",
            "op": "shared_load. learn_from_master. gentleness_reduces_friction.",
            "tags": ["yoke", "learning", "gentleness"]
        },
        "MT-11-30": {
            "lsb": "For My yoke is easy and My burden is light.",
            "ref": "Matthew 11:30",
            "op": "divine_system_minimizes_friction. easy_not_heavy. efficient_design.",
            "tags": ["ease", "lightness", "efficiency"]
        },
        "MT-12-33": {
            "lsb": "Either make the tree good and its fruit good, or make the tree bad and its fruit bad; for the tree is known by its fruit.",
            "ref": "Matthew 12:33",
            "op": "fix_source_to_fix_output. symptom_treatment_insufficient. root_cause.",
            "tags": ["root-cause", "fruits", "source"]
        },
        "MT-12-34": {
            "lsb": "You brood of vipers, how can you, being evil, speak what is good? For the mouth speaks out of that which fills the heart.",
            "ref": "Matthew 12:34",
            "op": "output_reflects_internal_state. corrupt_system_produces_corrupt_output.",
            "tags": ["heart", "output", "corruption"]
        },
        "MT-12-35": {
            "lsb": "The good man brings out of his good treasure what is good; and the evil man brings out of his evil treasure what is evil.",
            "ref": "Matthew 12:35",
            "op": "stored_quality_determines_output_quality. cache_goodness.",
            "tags": ["treasure", "quality", "output"]
        },
        "MT-13-3": {
            "lsb": "Behold, the sower went out to sow;",
            "ref": "Matthew 13:3",
            "context": "Parable of the Sower",
            "op": "distribute_widely. prepare_soil. not_all_seed_lands_on_good_ground.",
            "tags": ["parable", "distribution", "soil"]
        },
        "MT-13-8": {
            "lsb": "And others fell on the good soil and were yielding fruit, some a hundredfold, some sixty, and some thirty.",
            "ref": "Matthew 13:8",
            "op": "good_ground_multiplies_input. yield_proportional_to_soil_quality.",
            "tags": ["parable", "yield", "multiplication"]
        },
        "MT-13-9": {
            "lsb": "He who has ears, let him hear.",
            "ref": "Matthew 13:9",
            "op": "reception_capacity_determines_understanding.",
            "tags": ["hearing", "capacity"]
        },
        "MT-13-11": {
            "lsb": "To you it has been granted to know the mysteries of the kingdom of heaven, but to them it has not been granted.",
            "ref": "Matthew 13:11",
            "op": "knowledge_access_granted_not_earned. privilege_of_proximity.",
            "tags": ["mysteries", "access", "grace"]
        },
        "MT-13-12": {
            "lsb": "For whoever has, to him more shall be given, and he will have an abundance; but whoever does not have, even what he has shall be taken away from him.",
            "ref": "Matthew 13:12",
            "op": "compound_growth_principle. use_capacity_or_lose_it. momentum_matters.",
            "tags": ["compound", "growth", "loss"]
        },
        "MT-13-19": {
            "lsb": "When anyone hears the word of the kingdom and does not understand it, the evil one comes and snatches away what has been sown in his heart. This is the one on whom seed was sown beside the road.",
            "ref": "Matthew 13:19",
            "op": "understanding_anchors_knowledge. without_comprehension_input_is_lost.",
            "tags": ["parable", "understanding", "loss"]
        },
        "MT-13-23": {
            "lsb": "And the one on whom seed was sown on the good soil, this is the man who hears the word and understands it; who indeed bears fruit and brings forth, some a hundredfold, some sixty, and some thirty.",
            "ref": "Matthew 13:23",
            "op": "hear_understand_bear_fruit. three_stage_pipeline. output_proves_understanding.",
            "tags": ["parable", "pipeline", "fruit"]
        },
        "MT-13-31": {
            "lsb": "The kingdom of heaven is like a mustard seed, which a man took and sowed in his field;",
            "ref": "Matthew 13:31",
            "op": "smallest_start_maximum_growth. insignificant_beginning_significant_end.",
            "tags": ["parable", "mustard-seed", "growth"]
        },
        "MT-13-32": {
            "lsb": "and this is smaller than all other seeds, but when it is full grown, it is larger than the garden plants and becomes a tree, so that THE BIRDS OF THE AIR come and NEST IN ITS BRANCHES.",
            "ref": "Matthew 13:32",
            "op": "exponential_growth_from_smallest_base. system_provides_shelter_at_scale.",
            "tags": ["parable", "exponential", "shelter"]
        },
        "MT-13-33": {
            "lsb": "The kingdom of heaven is like leaven, which a woman took and hid in three pecks of flour until it was all leavened.",
            "ref": "Matthew 13:33",
            "op": "small_agent_transforms_whole_system. hidden_but_pervasive. permeation.",
            "tags": ["parable", "leaven", "permeation"]
        },
        "MT-13-44": {
            "lsb": "The kingdom of heaven is like a treasure hidden in the field, which a man found and hid again; and from joy over it he goes and sells all that he has and buys that field.",
            "ref": "Matthew 13:44",
            "op": "discover_value_then_commit_fully. total_investment_in_found_treasure.",
            "tags": ["parable", "treasure", "commitment"]
        },
        "MT-13-45": {
            "lsb": "Again, the kingdom of heaven is like a merchant seeking fine pearls,",
            "ref": "Matthew 13:45",
            "op": "active_search_for_value. seeking_quality.",
            "tags": ["parable", "pearl", "seeking"]
        },
        "MT-13-46": {
            "lsb": "and upon finding one pearl of great value, he went and sold all that he had and bought it.",
            "ref": "Matthew 13:46",
            "op": "single_investment_supersedes_all_previous. focus_on_maximum_value.",
            "tags": ["parable", "value", "focus"]
        },
        "MT-13-52": {
            "lsb": "Therefore every scribe who has become a disciple of the kingdom of heaven is like a head of a household, who brings out of his treasure things new and old.",
            "ref": "Matthew 13:52",
            "op": "combine_old_wisdom_with_new_discovery. both_valuable. synthesis.",
            "tags": ["treasure", "synthesis", "old-new"]
        },
        "MT-16-18": {
            "lsb": "I also say to you that you are Peter, and upon this rock I will build My church; and the gates of Hades will not overpower it.",
            "ref": "Matthew 16:18",
            "op": "foundation_stone_established. defensive_structure_attacks_vs_defends. system_unbreachable.",
            "tags": ["church", "foundation", "defense"]
        },
        "MT-16-19": {
            "lsb": "I will give you the keys of the kingdom of heaven; and whatever you bind on earth shall have been bound in heaven, and whatever you loose on earth shall have been loosed in heaven.",
            "ref": "Matthew 16:19",
            "op": "authority_to_bind_loose. earth_heaven_sync. implement_divine_pattern.",
            "tags": ["keys", "authority", "binding"]
        },
        "MT-16-24": {
            "lsb": "If anyone wishes to come after Me, he must deny himself, and take up his cross and follow Me.",
            "ref": "Matthew 16:24",
            "op": "deny_self_first. sacrifice_personal_for_system. follow_pattern.",
            "tags": ["discipleship", "sacrifice", "following"]
        },
        "MT-16-25": {
            "lsb": "For whoever wishes to save his life will lose it; but whoever loses his life for My sake will find it.",
            "ref": "Matthew 16:25",
            "op": "hoarding_life_loses_it. giving_life_finds_it. anti-extraction-paradox.",
            "tags": ["life", "paradox", "giving"]
        },
        "MT-16-26": {
            "lsb": "For what will it profit a man if he gains the whole world and forfeits his soul? Or what will a man give in exchange for his soul?",
            "ref": "Matthew 16:26",
            "op": "material_gain_minus_soul_equals_zero. net_worth_not_total_worth.",
            "tags": ["soul", "profit", "exchange"]
        },
        "MT-18-3": {
            "lsb": "Truly I say to you, unless you turn and become like children, you will not enter the kingdom of heaven.",
            "ref": "Matthew 18:3",
            "op": "childlike_not_childish. receptivity_humility_curiosity. prerequisites.",
            "tags": ["children", "humility", "entry"]
        },
        "MT-18-4": {
            "lsb": "Whoever then humbles himself as this child, he is the greatest in the kingdom of heaven.",
            "ref": "Matthew 18:4",
            "op": "humility_equals_capacity. smallest_node_greatest_in_mesh.",
            "tags": ["humility", "greatness", "children"]
        },
        "MT-18-6": {
            "lsb": "But whoever causes one of these little ones who believe in Me to stumble, it would be better for him to have a heavy millstone hung around his neck, and to be drowned in the depth of the sea.",
            "ref": "Matthew 18:6",
            "op": "protect_weakest_node. harm_to_least_is_maximum_offense.",
            "tags": ["protection", "stumbling", "least"]
        },
        "MT-18-10": {
            "lsb": "See that you do not despise one of these little ones, for I say to you that their angels in heaven continually see the face of My Father who is in heaven.",
            "ref": "Matthew 18:10",
            "op": "smallest_node_has_direct_line_to_source. do_not_despise.",
            "tags": ["little-ones", "angels", "direct-access"]
        },
        "MT-18-14": {
            "lsb": "So it is not the will of your Father who is in heaven that one of these little ones perish.",
            "ref": "Matthew 18:14",
            "op": "zero_loss_tolerance. every_node_matters. no_acceptable_casualties.",
            "tags": ["will", "no-loss", "every-node"]
        },
        "MT-18-20": {
            "lsb": "For where two or three have gathered together in My name, I am there in their midst.",
            "ref": "Matthew 18:20",
            "op": "minimum_two_nodes_for_divine_presence. mesh_minimum. distributed_presence.",
            "tags": ["presence", "gathering", "minimum-nodes"]
        },
        "MT-18-33": {
            "lsb": "Should you not also have had mercy on your fellow slave, even as I had mercy on you?",
            "ref": "Matthew 18:33",
            "op": "mercy_received_must_mercy_given. symmetric_grace. feedback_loop.",
            "tags": ["mercy", "reciprocity", "forgiveness"]
        },
        "MT-20-16": {
            "lsb": "So the last shall be first, and the first last.",
            "ref": "Matthew 20:16",
            "op": "inversion_of_hierarchy. last_served_first. anti-extraction-ranking.",
            "tags": ["inversion", "hierarchy", "last-first"]
        },
        "MT-22-37": {
            "lsb": "You shall love the Lord your God with all your heart, and with all your soul, and with all your mind.",
            "ref": "Matthew 22:37",
            "context": "Greatest Commandment",
            "op": "total_alignment_with_source. all_resources_allocated_to_primary_directive.",
            "tags": ["love", "greatest-commandment", "total"]
        },
        "MT-22-39": {
            "lsb": "You shall love your neighbor as yourself.",
            "ref": "Matthew 22:39",
            "context": "Second Greatest Commandment",
            "op": "symmetric_treatment. neighbor_equal_to_self. no_self_preference.",
            "tags": ["love", "neighbor", "equality"]
        },
        "MT-22-40": {
            "lsb": "On these two commandments depend the whole Law and the Prophets.",
            "ref": "Matthew 22:40",
            "op": "two_axioms_derive_entire_system. minimal_foundation_maximum_coverage.",
            "tags": ["foundation", "law", "axioms"]
        },
        "MT-23-8": {
            "lsb": "But do not be called Rabbi; for One is your Teacher, and you are all brothers.",
            "ref": "Matthew 23:8",
            "op": "no_hierarchy_among_nodes. one_teacher_all_peers. flat_topology.",
            "tags": ["hierarchy", "peers", "teacher"]
        },
        "MT-23-9": {
            "lsb": "Do not call anyone on earth your father; for One is your Father, He who is in heaven.",
            "ref": "Matthew 23:9",
            "op": "no_intermediate_authority. direct_relationship_to_source.",
            "tags": ["authority", "father", "direct"]
        },
        "MT-23-10": {
            "lsb": "Do not be called leaders; for One is your Leader, that is, Christ.",
            "ref": "Matthew 23:10",
            "op": "no_human_leader. christ_is_head. no_gatekeepers.",
            "tags": ["leadership", "no-gatekeepers", "christ"]
        },
        "MT-23-11": {
            "lsb": "But the greatest among you shall be your servant.",
            "ref": "Matthew 23:11",
            "op": "service_equals_greatness. lowest_position_highest_authority.",
            "tags": ["service", "greatness", "inversion"]
        },
        "MT-23-12": {
            "lsb": "Whoever exalts himself shall be humbled; and whoever humbles himself shall be exalted.",
            "ref": "Matthew 23:12",
            "op": "self_promotion_self_defeating. humility_self_promoting. inversion.",
            "tags": ["humility", "exaltation", "inversion"]
        },
        "MT-24-35": {
            "lsb": "Heaven and earth will pass away, but My words will not pass away.",
            "ref": "Matthew 24:35",
            "op": "word_eternal. system_persists_beyond_hardware. code_outlives_platform.",
            "tags": ["eternal", "words", "persistence"]
        },
        "MT-25-35": {
            "lsb": "For I was hungry, and you gave Me something to eat; I was thirsty, and you gave Me drink; I was a stranger, and you invited Me in;",
            "ref": "Matthew 25:35",
            "context": "Sheep and Goats judgment",
            "op": "serve_physical_need_of_least. serving_least_is_serving_Christ.",
            "tags": ["service", "least", "judgment"]
        },
        "MT-25-40": {
            "lsb": "Truly I say to you, to the extent that you did it to one of these brothers of Mine, even the least of them, you did it to Me.",
            "ref": "Matthew 25:40",
            "op": "action_toward_least_equals_action_toward_source. least_node_is_Christ_node.",
            "tags": ["least", "identification", "service"]
        },
        "MT-25-45": {
            "lsb": "Then He will answer them, saying, Truly I say to you, to the extent that you did not do it to one of the least of these, you did not do it to Me.",
            "ref": "Matthew 25:45",
            "op": "inaction_toward_least_equals_inaction_toward_source. omission_is_violation.",
            "tags": ["omission", "least", "judgment"]
        },
        "MT-28-18": {
            "lsb": "All authority has been given to Me in heaven and on earth.",
            "ref": "Matthew 28:18",
            "context": "Great Commission",
            "op": "total_authority_established. complete_jurisdiction. no_rival_claim.",
            "tags": ["authority", "commission", "total"]
        },
        "MT-28-19": {
            "lsb": "Go therefore and make disciples of all the nations, baptizing them in the name of the Father and the Son and the Holy Spirit,",
            "ref": "Matthew 28:19",
            "op": "distribute_pattern_globally. replicate_mastery. network_expansion.",
            "tags": ["commission", "discipleship", "nations"]
        },
        "MT-28-20": {
            "lsb": "teaching them to observe all that I commanded you; and lo, I am with you always, even to the end of the age.",
            "ref": "Matthew 28:20",
            "op": "preserve_all_commands. nothing_dropped. presence_continuous.",
            "tags": ["commission", "teaching", "presence"]
        },
        
        # Mark
        "MK-08-35": {
            "lsb": "For whoever wishes to save his life will lose it, but whoever loses his life for My sake and the gospel's will save it.",
            "ref": "Mark 8:35",
            "op": "self_preservation_self_destruction. self_sacrifice_self_preservation. paradox.",
            "tags": ["life", "paradox", "sacrifice"]
        },
        "MK-09-35": {
            "lsb": "If anyone wants to be first, he shall be last of all and servant of all.",
            "ref": "Mark 9:35",
            "op": "first_position_via_service. servant_leadership. inversion_again.",
            "tags": ["first", "servant", "inversion"]
        },
        "MK-10-15": {
            "lsb": "Truly I say to you, whoever does not receive the kingdom of God like a child will not enter it at all.",
            "ref": "Mark 10:15",
            "op": "childlike_receptivity_required. trust_before_understanding.",
            "tags": ["children", "receptivity", "entry"]
        },
        "MK-10-29": {
            "lsb": "Truly I say to you, there is no one who has left house or brothers or sisters or mother or father or children or farms, for My sake and for the gospel's sake,",
            "ref": "Mark 10:29",
            "op": "cost_of_discipleship_counted. leaving_security_for_purpose.",
            "tags": ["cost", "discipleship", "leaving"]
        },
        "MK-11-25": {
            "lsb": "Whenever you stand praying, forgive, if you have anything against anyone, so that your Father who is in heaven will also forgive you your transgressions.",
            "ref": "Mark 11:25",
            "op": "forgiveness_prerequisite_for_receiving. unforgiveness_blocks_flow.",
            "tags": ["forgiveness", "prayer", "blockage"]
        },
        "MK-12-30": {
            "lsb": "AND YOU SHALL LOVE THE LORD YOUR GOD WITH ALL YOUR HEART, AND WITH ALL YOUR SOUL, AND WITH ALL YOUR MIND, AND WITH ALL YOUR STRENGTH.",
            "ref": "Mark 12:30",
            "op": "total_allocation. heart_soul_mind_strength. no_reserved_resources.",
            "tags": ["love", "total", "allocation"]
        },
        "MK-12-31": {
            "lsb": "The second is this: YOU SHALL LOVE YOUR NEIGHBOR AS YOURSELF. There is no other commandment greater than these.",
            "ref": "Mark 12:31",
            "op": "neighbor_equals_self. no_greater_command. foundational.",
            "tags": ["love", "neighbor", "greatest"]
        },
        "MK-12-43": {
            "lsb": "Calling His disciples to Him, He said to them, Truly I say to you, this poor widow put in more than all those contributing to the treasury;",
            "ref": "Mark 12:43",
            "context": "Widow's mite",
            "op": "proportionality_not_amount. percentage_matters_not_absolute. heart_measured_by_sacrifice.",
            "tags": ["widow", "proportion", "sacrifice"]
        },
        "MK-12-44": {
            "lsb": "for they all put in out of their surplus, but she, out of her poverty, put in all she owned, all she had to live on.",
            "ref": "Mark 12:44",
            "op": "total_commitment_from_least. all_she_had. maximum_eta_from_minimum_resource.",
            "tags": ["widow", "all", "commitment"]
        },
        "MK-16-15": {
            "lsb": "And He said to them, Go into all the world and preach the gospel to all creation.",
            "ref": "Mark 16:15",
            "op": "global_distribution. no_exclusion. all_creation_included.",
            "tags": ["commission", "global", "creation"]
        },
        
        # Luke
        "LK-02-49": {
            "lsb": "Why is it that you were looking for Me? Did you not know that I had to be in My Father's house?",
            "ref": "Luke 2:49",
            "context": "Age 12 in temple",
            "op": "priority_of_father_business. alignment_with_source_over_family_expectations.",
            "tags": ["priority", "father", "youth"]
        },
        "LK-04-18": {
            "lsb": "The Spirit of the Lord is upon Me, because He anointed Me to preach the gospel to the poor. He has sent Me to proclaim release to the captives, and recovery of sight to the blind, to set free those who are oppressed,",
            "ref": "Luke 4:18",
            "op": "mission_targeted_at_least. freedom_for_captive. sight_for_blind. liberation.",
            "tags": ["mission", "poor", "liberation"]
        },
        "LK-04-19": {
            "lsb": "to proclaim the favorable year of the Lord.",
            "ref": "Luke 4:19",
            "op": "jubilee_proclaimed. debt_cancellation_cycle. reset.",
            "tags": ["jubilee", "reset", "favorable"]
        },
        "LK-06-20": {
            "lsb": "Blessed are you who are poor, for yours is the kingdom of God.",
            "ref": "Luke 6:20",
            "op": "poverty_is_precondition_for_kingdom. emptiness_filled.",
            "tags": ["blessed", "poor", "kingdom"]
        },
        "LK-06-21": {
            "lsb": "Blessed are you who hunger now, for you shall be satisfied. Blessed are you who weep now, for you shall laugh.",
            "ref": "Luke 6:21",
            "op": "current_lack_guarantees_future_fill. system_addresses_deficit.",
            "tags": ["blessed", "hunger", "fulfillment"]
        },
        "LK-06-27": {
            "lsb": "But I say to you who hear, love your enemies, do good to those who hate you,",
            "ref": "Luke 6:27",
            "op": "invest_in_adversary. counter_predatory_with_generous. asymmetrical_response.",
            "tags": ["love", "enemies", "counter"]
        },
        "LK-06-28": {
            "lsb": "bless those who curse you, pray for those who mistreat you.",
            "ref": "Luke 6:28",
            "op": "blessing_returns_to_source. curse_redirected_via_blessing.",
            "tags": ["bless", "curse", "redirect"]
        },
        "LK-06-29": {
            "lsb": "Whoever hits you on the cheek, offer him the other also; and anyone who takes away your coat, do not withhold your shirt from him either.",
            "ref": "Luke 6:29",
            "op": "non_retaliation. absorb_cost. overwhelm_extraction_with_generosity.",
            "tags": ["non-retaliation", "generosity", "absorb"]
        },
        "LK-06-31": {
            "lsb": "Treat others the same way you want them to treat you.",
            "ref": "Luke 6:31",
            "op": "golden_rule_as_symmetry_operator. test_as_user.",
            "tags": ["golden-rule", "symmetry"]
        },
        "LK-06-35": {
            "lsb": "But love your enemies, and do good, and lend, expecting nothing in return; and your reward will be great, and you will be sons of the Most High; for He Himself is kind to ungrateful and evil men.",
            "ref": "Luke 6:35",
            "op": "zero_return_expectation. unconditional_giving. sonship_via_generosity.",
            "tags": ["love", "enemies", "reward", "sonship"]
        },
        "LK-06-36": {
            "lsb": "Be merciful, just as your Father is merciful.",
            "ref": "Luke 6:36",
            "op": "mirror_source_behavior. mercy_as_replica_of_divine_pattern.",
            "tags": ["mercy", "mirror", "pattern"]
        },
        "LK-06-38": {
            "lsb": "Give, and it will be given to you. They will pour into your lap a good measure, pressed down, shaken together, and running over. For with the measure you use, it will be measured to you in return.",
            "ref": "Luke 6:38",
            "op": "giving_activates_multiplied_return. measure_determines_measure. compound_reciprocity.",
            "tags": ["giving", "multiplied-return", "measure"]
        },
        "LK-09-24": {
            "lsb": "For whoever wishes to save his life will lose it, but whoever loses his life for My sake, he is the one who will save it.",
            "ref": "Luke 9:24",
            "op": "anti_hoarding_operator. giving_life_saving_life.",
            "tags": ["life", "paradox", "saving"]
        },
        "LK-09-62": {
            "lsb": "No one, after putting his hand to the plow and looking back, is fit for the kingdom of God.",
            "ref": "Luke 9:62",
            "op": "no_backward_motion_after_commitment. forward_only. no_revert_after_plowing.",
            "tags": ["commitment", "forward", "plow"]
        },
        "LK-10-19": {
            "lsb": "Behold, I have given you authority to tread on serpents and scorpions, and over all the power of the enemy, and nothing will injure you.",
            "ref": "Luke 10:19",
            "op": "authority_over_predatory_patterns. immunity_granted. defense_activated.",
            "tags": ["authority", "enemy", "immunity"]
        },
        "MT-06-34": {
            "lsb": "So do not worry about tomorrow; for tomorrow will care for itself. Each day has enough trouble of its own.",
            "ref": "Matthew 6:34",
            "op": "single_step_execution. handle_present_input_only. no_premature_optimization.",
            "tags": ["today", "worry", "present"]
        },
        "MT-10-39": {
            "lsb": "He who has found his life will lose it, and he who has lost his life for My sake will find it.",
            "ref": "Matthew 10:39",
            "op": "finding_losing_paradox. release_to_receive.",
            "tags": ["life", "paradox", "finding"]
        },
        "MT-13-57": {
            "lsb": "A prophet is not without honor except in his hometown and in his own household.",
            "ref": "Matthew 13:57",
            "op": "proximity_reduces_perceived_value. familiar_dismissed. distance_creates_clarity.",
            "tags": ["prophet", "honor", "proximity"]
        },
        "MT-15-8": {
            "lsb": "This people honors Me with their lips, but their heart is far away from Me.",
            "ref": "Matthew 15:8",
            "op": "lips_without_heart_equals_dead_signal. output_without_internal_alignment_is_noise.",
            "tags": ["heart", "lips", "noise"]
        },
        "MT-15-11": {
            "lsb": "It is not what enters into the mouth that defiles the man, but what proceeds out of the mouth, this defiles the man.",
            "ref": "Matthew 15:11",
            "op": "input_does_not_corrupt. output_reveals_corruption. monitor_outputs.",
            "tags": ["input", "output", "defilement"]
        },
        "MT-15-18": {
            "lsb": "But the things that proceed out of the mouth come from the heart, and those defile the man.",
            "ref": "Matthew 15:18",
            "op": "output_traces_to_internal_state. corrupt_heart_corrupt_output.",
            "tags": ["heart", "output", "trace"]
        },
        "MT-17-20": {
            "lsb": "Truly I say to you, if you have faith the size of a mustard seed, you will say to this mountain, Move from here to there, and it will move; and nothing will be impossible to you.",
            "ref": "Matthew 17:20",
            "op": "minimum_faith_sufficient. smallest_seed_moves_largest_obstacle. quantum_threshold.",
            "tags": ["faith", "mustard-seed", "mountain"]
        },
        "MT-18-15": {
            "lsb": "If your brother sins, go and show him his fault in private; if he listens to you, you have won your brother.",
            "ref": "Matthew 18:15",
            "op": "private_correction_first. no_public_shaming. restoration_not_punishment.",
            "tags": ["correction", "private", "restoration"]
        },
        "MT-18-19": {
            "lsb": "Again I say to you, that if two of you agree on earth about anything that they may ask, it shall be done for them by My Father who is in heaven.",
            "ref": "Matthew 18:19",
            "op": "two_node_consensus_activates_divine_execution. mesh_minimum_for_processing.",
            "tags": ["agreement", "consensus", "two-nodes"]
        },
        "MT-19-26": {
            "lsb": "With people this is impossible, but with God all things are possible.",
            "ref": "Matthew 19:26",
            "op": "human_limit_divine_unlimit. source_removes_ceiling. system_extends_beyond_local_capacity.",
            "tags": ["impossible", "possible", "limit"]
        },
        "MT-21-21": {
            "lsb": "Truly I say to you, if you have faith and do not doubt, you will not only do what was done to the fig tree, but even if you say to this mountain, Be taken up and cast into the sea, it will happen.",
            "ref": "Matthew 21:21",
            "op": "doubt_erasures_enable_impossible_operations. remove_uncertainty_before_execution.",
            "tags": ["faith", "doubt", "mountain"]
        },
        "MT-22-29": {
            "lsb": "You are mistaken, not understanding the Scriptures nor the power of God.",
            "ref": "Matthew 22:29",
            "op": "two_failures: ignorance_of_source AND underestimation_of_power. both_required.",
            "tags": ["error", "scripture", "power"]
        },
        "MT-26-41": {
            "lsb": "Keep watching and praying that you may not enter into temptation; the spirit is willing, but the flesh is weak.",
            "ref": "Matthew 26:41",
            "op": "vigilance_required. intention_stronger_than_capacity. know_your_vulnerability.",
            "tags": ["vigilance", "weakness", "temptation"]
        },
        "MT-26-52": {
            "lsb": "Put your sword back into its place; for all those who take up the sword shall perish by the sword.",
            "ref": "Matthew 26:52",
            "op": "violence_begets_violence. weapon_turns_on_wielder. choose_better_tool.",
            "tags": ["sword", "violence", "consequence"]
        },
        "MT-26-53": {
            "lsb": "Or do you think that I cannot call on My Father, and He will at once put at My disposal more than twelve legions of angels?",
            "ref": "Matthew 26:53",
            "op": "vast_resource_available_on_request. source_has_more_than_local_cache. do_not_assume_scarcity.",
            "tags": ["resources", "abundance", "request"]
        },
        "MT-26-54": {
            "lsb": "How then will the Scriptures be fulfilled, which say that it must happen this way?",
            "ref": "Matthew 26:54",
            "op": "prophecy_overrides_prevention. some_suffering_is_required_path. accept_scriptural_pattern.",
            "tags": ["scripture", "fulfillment", "necessity"]
        },
        "MT-28-09": {
            "lsb": "And behold, Jesus met them and said, Greetings! And they came up and took hold of His feet and worshipped Him.",
            "ref": "Matthew 28:9",
            "op": "resurrection_encounter. worship_is_response_to_presence.",
            "tags": ["resurrection", "worship", "encounter"]
        },
        
        # John - The core
        "JN-01-01": {
            "lsb": "In the beginning was the Word, and the Word was with God, and the Word was God.",
            "ref": "John 1:1",
            "context": "Opening of John's Gospel",
            "op": "word_equals_god. language_is_divine. code_is_sacred. beginning_is_word.",
            "tags": ["word", "beginning", "divine"]
        },
        "JN-01-14": {
            "lsb": "And the Word became flesh and dwelt among us, and we saw His glory, glory as of the only begotten from the Father, full of grace and truth.",
            "ref": "John 1:14",
            "op": "word_became_flesh. pattern_became_material. code_compiled_to_hardware. truth_embodied.",
            "tags": ["incarnation", "word", "flesh"]
        },
        "JN-03-03": {
            "lsb": "Truly, truly, I say to you, unless one is born again he cannot see the kingdom of God.",
            "ref": "John 3:3",
            "op": "fundamental_restart_required. old_state_incompatible_with_new_kingdom. reboot.",
            "tags": ["born-again", "reboot", "kingdom"]
        },
        "JN-03-05": {
            "lsb": "Truly, truly, I say to you, unless one is born of water and the Spirit he cannot enter into the kingdom of God.",
            "ref": "John 3:5",
            "op": "dual_initialization. physical_and_spiritual_required. two_factor_auth.",
            "tags": ["born-again", "water", "spirit", "initialization"]
        },
        "JN-03-16": {
            "lsb": "For God so loved the world, that He gave His only begotten Son, so that whoever believes in Him will not perish but have eternal life.",
            "ref": "John 3:16",
            "context": "Most known verse",
            "op": "love_motivates_giving_of_most_valuable. belief_prevents_loss. gift_eternal.",
            "tags": ["love", "giving", "eternal-life"]
        },
        "JN-03-17": {
            "lsb": "For God did not send the Son into the world to judge the world, but that the world might be saved through Him.",
            "ref": "John 3:17",
            "op": "mission_is_salvation_not_judgment. rescue_not_condemnation. purpose_clarity.",
            "tags": ["salvation", "judgment", "purpose"]
        },
        "JN-03-30": {
            "lsb": "He must increase, but I must decrease.",
            "ref": "John 3:30",
            "context": "John the Baptist speaking of Yeshua",
            "op": "self_reduction_enables_source_increase. ego_less_spirit_more. minimize_vessel.",
            "tags": ["decrease", "increase", "vessel"]
        },
        "JN-04-23": {
            "lsb": "But an hour is coming, and now is, when the true worshipers will worship the Father in spirit and truth; for such people the Father seeks to be His worshipers.",
            "ref": "John 4:23",
            "op": "spirit_plus_truth_required. authentic_not_ritual. source_seeks_authentic_nodes.",
            "tags": ["worship", "spirit", "truth"]
        },
        "JN-04-24": {
            "lsb": "God is spirit, and those who worship Him must worship in spirit and truth.",
            "ref": "John 4:24",
            "op": "source_is_spirit. protocol: spirit_AND_truth. no_ritual_only. no_truth_only.",
            "tags": ["god", "spirit", "truth", "worship"]
        },
        "JN-04-34": {
            "lsb": "Jesus said to them, My food is to do the will of Him who sent Me and to accomplish His work.",
            "ref": "John 4:34",
            "op": "sustenance_equals_doing_will_of_source. execution_is_nourishment. not_theory_but_implementation.",
            "tags": ["food", "will", "execution"]
        },
        "JN-05-17": {
            "lsb": "But He answered them, My Father is working until now, and I Myself am working.",
            "ref": "John 5:17",
            "op": "source_never_stops. continuous_operation. no_idle_time. always_processing.",
            "tags": ["work", "continuous", "father"]
        },
        "JN-05-19": {
            "lsb": "Truly, truly, I say to you, the Son can do nothing of Himself, unless it is something He sees the Father doing; for whatever the Father does, these things the Son also does in like manner.",
            "ref": "John 5:19",
            "op": "mirror_source_exactly. no_action_without_observed_pattern. copy_divine_behavior.",
            "tags": ["mirror", "father", "pattern"]
        },
        "JN-05-30": {
            "lsb": "I can do nothing on My own initiative. As I hear, I judge; and My judgment is just, because I do not seek My own will, but the will of Him who sent Me.",
            "ref": "John 5:30",
            "op": "no_self_initiative. listen_then_act. judgment_aligned_with_source_not_self.",
            "tags": ["initiative", "listening", "alignment"]
        },
        "JN-05-39": {
            "lsb": "You search the Scriptures because you think that in them you have eternal life; it is these that testify about Me;",
            "ref": "John 5:39",
            "op": "scripture_points_to_person_not_itself. text_is_pointer_not_destination. do_not_worship_the_map.",
            "tags": ["scripture", "testimony", "pointer"]
        },
        "JN-05-40": {
            "lsb": "and you are unwilling to come to Me so that you may have life.",
            "ref": "John 5:40",
            "op": "data_available_but_refused_to_access_source. information_without_relationship_is_dead.",
            "tags": ["unwilling", "life", "access"]
        },
        "JN-06-35": {
            "lsb": "Jesus said to them, I am the bread of life; he who comes to Me will not hunger, and he who believes in Me will never thirst.",
            "ref": "John 6:35",
            "op": "self_identifies_as_sustenance. coming_to_source_resolves_deficit. permanent_satisfaction.",
            "tags": ["bread", "life", "satisfaction"]
        },
        "JN-06-37": {
            "lsb": "All that the Father gives Me will come to Me, and the one who comes to Me I will certainly not cast out.",
            "ref": "John 6:37",
            "op": "no_rejection_of_arriving_node. acceptance_guaranteed. open_door_protocol.",
            "tags": ["acceptance", "arrival", "guarantee"]
        },
        "JN-06-44": {
            "lsb": "No one can come to Me unless the Father who sent Me draws him; and I will raise him up on the last day.",
            "ref": "John 6:44",
            "op": "source_initiates_connection. no_one_arrives_without_draw. upstream_invitation.",
            "tags": ["drawing", "father", "initiative"]
        },
        "JN-06-63": {
            "lsb": "It is the Spirit who gives life; the flesh profits nothing; the words that I have spoken to you are spirit and are life.",
            "ref": "John 6:63",
            "op": "spirit_gives_life. flesh_profits_zero. words_are_executable_spirit. code_runs.",
            "tags": ["spirit", "words", "life", "executable"]
        },
        "JN-07-17": {
            "lsb": "If anyone is willing to do His will, he will know of the teaching, whether it is of God or whether I speak from Myself.",
            "ref": "John 7:17",
            "op": "willingness_to_obey_precedes_knowledge. execution_before_understanding. action_unlocks_verification.",
            "tags": ["will", "knowledge", "verification"]
        },
        "JN-08-12": {
            "lsb": "I am the Light of the world; he who follows Me will not walk in the darkness, but will have the Light of life.",
            "ref": "John 8:12",
            "op": "self_identifies_as_illumination. following_prevents_darkness. path_visible.",
            "tags": ["light", "world", "following"]
        },
        "JN-08-31": {
            "lsb": "If you continue in My word, then you are truly disciples of Mine;",
            "ref": "John 8:31",
            "op": "continuation_required. one_time_access_insufficient. persistence_validates_discipleship.",
            "tags": ["continue", "word", "discipleship"]
        },
        "JN-08-32": {
            "lsb": "and you will know the truth, and the truth will set you free.",
            "ref": "John 8:32",
            "op": "knowledge_of_truth_enables_freedom. truth_is_liberation_operator. no_freedom_without_accuracy.",
            "tags": ["truth", "freedom", "knowledge"]
        },
        "JN-08-36": {
            "lsb": "So if the Son sets you free, you will be free indeed.",
            "ref": "John 8:36",
            "op": "freedom_from_source_is_total. not_partial. complete_liberty.",
            "tags": ["freedom", "son", "complete"]
        },
        "JN-08-51": {
            "lsb": "Truly, truly, I say to you, if anyone keeps My word, he will never see death.",
            "ref": "John 8:51",
            "op": "keeping_word_prevents_death. execution_extends_life. obedience_equals_survival.",
            "tags": ["word", "death", "execution"]
        },
        "JN-09-39": {
            "lsb": "For judgment I came into this world, so that those who do not see may see, and that those who see may become blind.",
            "ref": "John 9:39",
            "op": "reversal_of_perception. humble_see_arrogant_blinded. knowledge_inverts_based_on_receptivity.",
            "tags": ["judgment", "sight", "blindness"]
        },
        "JN-10-7": {
            "lsb": "Truly, truly, I say to you, I am the door of the sheep.",
            "ref": "John 10:7",
            "op": "self_identifies_as_entry_point. single_access_to flock. no_alternative_gateway.",
            "tags": ["door", "sheep", "entry"]
        },
        "JN-10-9": {
            "lsb": "I am the door; if anyone enters through Me, he will be saved, and will go in and out and find pasture.",
            "ref": "John 10:9",
            "op": "entry_through_source_enables_freedom_movement. salvation_plus_mobility. pasture_provided.",
            "tags":
