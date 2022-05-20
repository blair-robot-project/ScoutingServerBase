from typing import Dict


def calc_quick_stats(fields, total) -> Dict[str, str]:
    """
    Calculate/filter the most necessary year-specific stats for a team

    Parameters:
    fields: A dictionary of the totals of some stats
    total: How many matches have been played

    Returns: A dictionary of only the most important stats
    """
    return fields


def calc_detailed_stats(fields, total) -> Dict[str, str]:
    """
    Calculate detailed year-specific stats for a team

    Parameters:
    fields: A dictionary of the totals of some stats
    total: How many matches have been played

    Returns: A dictionary of the original stats augmented with extra stats
    """
    fields.update({})
    return fields
