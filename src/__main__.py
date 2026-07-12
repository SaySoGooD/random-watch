from src.main.dependency_injection import container

if __name__ == "__main__":
    await container.init_resources()

    use_case = container.get_random_collection_usecase()
