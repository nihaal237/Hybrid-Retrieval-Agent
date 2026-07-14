from src.memory_system import MemorySystem

ms = MemorySystem()
result = ms.query("What's James's job?")
print("Answer:", result["answer"])
print("Routing:", result["routing"]["path"])