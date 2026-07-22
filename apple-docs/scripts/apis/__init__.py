"""
Apple Documentation APIs
========================

Standalone implementations for use in the sandbox.
These make direct HTTP calls - no external dependencies.
"""

from .apple_docs import fetch_documentation, search_apple_online_urls, get_framework_info
from .swift_evolution import search_proposals, get_proposal, search_swift_forums_urls, search_swift_forums
from .swift_repos import search_swift_repos_urls, fetch_github_file
from .wwdc_notes import search_wwdc_sessions, fetch_wwdc_session
from .hig import search_hig, fetch_hig
from .archive import (
    search_archive, list_archive_frameworks, list_archive_topics,
    list_archive_resource_types,
)
from .swift_compiler import (
    search_compiler_docs, search_compiler_docs_text,
    list_compiler_phases, get_compiler_phase,
)
from .xcode_releases import list_xcode_release_notes, get_xcode_release_notes_url
from .authority import get_source_authority
from .project_context import configure_project_root, detect_apple_project_context
from .local_xcode_docs import (
    fetch_local_xcode_doc,
    list_xcode_documentation_sources,
    search_local_xcode_docs,
)

__all__ = [
    'fetch_documentation',
    'search_apple_online_urls',
    'get_framework_info',
    'search_proposals',
    'get_proposal',
    'search_swift_forums_urls',
    'search_swift_forums',
    'search_swift_repos_urls',
    'fetch_github_file',
    'search_wwdc_sessions',
    'fetch_wwdc_session',
    'search_hig',
    'fetch_hig',
    'search_archive',
    'list_archive_frameworks',
    'list_archive_topics',
    'list_archive_resource_types',
    'search_compiler_docs',
    'search_compiler_docs_text',
    'list_compiler_phases',
    'get_compiler_phase',
    'list_xcode_release_notes',
    'get_xcode_release_notes_url',
    'get_source_authority',
    'detect_apple_project_context',
    'list_xcode_documentation_sources',
    'search_local_xcode_docs',
    'fetch_local_xcode_doc',
]


def configure(project_root='.'):
    """Configure host-owned context. This function is not exposed in the sandbox."""
    configure_project_root(project_root)
