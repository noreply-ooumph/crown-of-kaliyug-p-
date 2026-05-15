def format_violations(violations):
    """
    Formats canon violations into a readable string.
    """
    if not violations:
        return "No violations found."
    
    report = ""
    for v in violations:
        report += f"- [{v.get('severity')}] {v.get('scene_id')}: {v.get('issue')}\n"
    return report

def format_violations_for_retry(violations):
    """
    Formats violations specifically for the Script Writer's retry context.
    """
    return format_violations(violations)
