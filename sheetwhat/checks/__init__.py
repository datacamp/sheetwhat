from sheetwhat.checks.check_funcs import has_code

# don't import some funcs from protowhat that don't make sense:
# - check_node, check_edge and has_equal_ast don't work well.
# - has_parsed_ast not necessary
# - has_code has its own implementation in sheetwhat
# - no check_file related functionality
from protowhat.checks.check_logic import fail, multi, check_not, check_or, check_correct
from protowhat.checks.check_simple import has_chosen, success_msg