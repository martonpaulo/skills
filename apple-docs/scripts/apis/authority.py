"""Source-authority metadata for Apple documentation research."""

SOURCE_AUTHORITY = (
    {
        "rank": 1,
        "source": "Official Apple documentation and release notes",
        "authority": "primary",
    },
    {
        "rank": 2,
        "source": "Official Apple or Swift source repositories",
        "authority": "primary",
    },
    {
        "rank": 3,
        "source": "Accepted Swift Evolution proposals",
        "authority": "primary_for_language_design",
    },
    {
        "rank": 4,
        "source": "Official WWDC pages and transcripts",
        "authority": "primary",
    },
    {
        "rank": 5,
        "source": "Apple Developer Forums and Swift Forums",
        "authority": "secondary",
    },
    {
        "rank": 6,
        "source": "Community-written WWDC notes or summaries",
        "authority": "community",
    },
)


def get_source_authority():
    """Return the ordered source policy exposed to sandboxed queries."""
    return {"sources": [dict(item) for item in SOURCE_AUTHORITY]}
