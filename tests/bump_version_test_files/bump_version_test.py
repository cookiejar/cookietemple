"""
This file provides various version numbers in python code that should be updated or not
for the bump version test cases
"""

# We start with the version in a comment: 0.0.0 that should be updated after bump
# BUT this one should not as 0.0.0 <<COOKIETEMPLE_NO_BUMP>> says no.


class BumpIt:
    a_class_var_version_should_bump = '0.0.0dev'
    a_class_var2_version_should_bump = 'v0.0.0'
    a_class_var3_version_should_bump = '0.0.0'

    a_class_var_version_no_bump = '0.0.0dev'  # <<COOKIETEMPLE_NO_BUMP>>
    a_class_var2_version_no_bump = 'v0.0.0'  # <<COOKIETEMPLE_NO_BUMP>>
    a_class_var3_version_no_bump = '0.0.0'  # <<COOKIETEMPLE_NO_BUMP>>

    def bump_or_dump(self, more: str, params: list) -> str:
        vers1 = '0.0.0dev'
        vers2 = '0.0.0'  # <<COOKIETEMPLE_NO_BUMP>>

        concat_those_versions = vers1 + vers2
        return concat_those_versions
