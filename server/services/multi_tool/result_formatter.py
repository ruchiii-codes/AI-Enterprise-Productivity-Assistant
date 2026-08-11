def format_multi_tool_results(results):
    sections = []

    for result in results:
        tool_name = result.get("tool", "unknown")

        if not result["success"]:
            sections.append(
                f"❌ {tool_name} failed\n\n{result['error']}"
            )
            continue

        data = result["result"]

        if "gmail" in tool_name:
            title = "📧 Gmail"
            content = str(data)

        elif "calendar" in tool_name:
            title = "📅 Calendar"
            content = str(data)

        elif "github" in tool_name:
            title = "🐙 GitHub"

            if isinstance(data, list):
                lines = ["Repositories:"]

                for index, repo in enumerate(data, start=1):
                    visibility = (
                        "Private" if repo.get("private") else "Public"
                    )

                    lines.append(
                        f"{index}. {repo.get('name')}\n"
                        f"   Visibility: {visibility}\n"
                        f"   {repo.get('url')}"
                    )

                content = "\n\n".join(lines)

            else:
                content = str(data)

        else:
            title = f"🔧 {tool_name}"
            content = str(data)

        sections.append(
            f"{title}\n\n{content}"
        )

    return "\n\n".join(sections)