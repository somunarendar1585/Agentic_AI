from mcp.server.fastmcp import FastMCP


server = FastMCP("Student Records")


@server.tool()
def get_student_marks(name: str) -> dict:
    """Find a student's marks in the sample student records."""
    students = {
        "ravi": 88,
        "sita": 92,
        "arun": 74,
    }

    student_name = name.strip().lower()
    marks = students.get(student_name)

    if marks is None:
        return {
            "student": student_name,
            "found": False,
        }

    return {
        "student": student_name,
        "found": True,
        "marks": marks,
    }


if __name__ == "__main__":
    server.run(transport="stdio")