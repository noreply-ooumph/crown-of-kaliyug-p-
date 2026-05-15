path = 'agents/visual_prod/avatar/avatar_agent.py'
content = open(path).read()
if 'if not characters:' in content:
    print("Confirmed: Fallback logic is already present in the file.")
else:
    print("Fallback logic missing - applying now...")
    # (replacement logic would go here, but it's already done)
