try:
            with open(f"saves/custom/models/{name}.txt", "w") as file:
                pass
        except:
            Path("saves/custom/models/").mkdir(parents=True, exist_ok=True)