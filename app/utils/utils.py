from typing import Optional


def generate_link_photo(uuid: Optional[str] = None) -> Optional[str]:
    if uuid:
        return f"https://foodsharing.shitposting.team/api/v1/documents/delivery/{uuid}.pdf"
    return None
