from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError


# database connection
def connect_db():
    try:
        client = MongoClient(
            "mongodb+srv://Moroz_Yevhen_db_user:pokenyxandEX36@task1.4zatt2b.mongodb.net/?appName=Task1",
            server_api=ServerApi('1')
        )
        db = client["Task_1"]
        collection = db["task_1"]
        return collection

    except PyMongoError as e:
        print(f"Connection error: {e}")
        return None


# create
def create_cat(collection, name, age, features):
    try:
        collection.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
        print("Cat added.")
    except PyMongoError as e:
        print(f"Insert error: {e}")


# read all
def read_all(collection):
    try:
        for cat in collection.find():
            print(cat)
    except PyMongoError as e:
        print(f"Read error: {e}")


# read by name
def read_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Cat not found.")
    except PyMongoError as e:
        print(f"Read error: {e}")


# update age
def update_age(collection, name, new_age):
    try:
        result = collection.update_one(
            {"name": name},
            {"$set": {"age": new_age}}
        )
        if result.matched_count:
            print("Age updated.")
        else:
            print("Cat not found.")
    except PyMongoError as e:
        print(f"Update error: {e}")


# add feature
def add_feature(collection, name, feature):
    try:
        result = collection.update_one(
            {"name": name},
            {"$push": {"features": feature}}
        )
        if result.matched_count:
            print("Feature added.")
        else:
            print("Cat not found.")
    except PyMongoError as e:
        print(f"Update error: {e}")


# delete by name
def delete_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Deleted")
        else:
            print("Cat not found.")
    except PyMongoError as e:
        print(f"Delete error: {e}")


# delete all
def delete_all(collection):
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents.")
    except PyMongoError as e:
        print(f"Delete error: {e}")


# input age with validation
def input_age():
    while True:
        try:
            age = int(input("Age: "))
            if age < 0:
                print("Age must be >= 0")
                continue
            return age
        except ValueError:
            print("Please enter a number!")


# input name with validation
def input_name():
    while True:
        name = input("Name: ").strip()

        if not name:
            print("Name cannot be empty!")
            continue

        if name.isdigit():
            print("Name cannot be only numbers!")
            continue

        return name


# input features with validation
def input_features():
    while True:
        features = input("Features (comma separated): ").strip()

        if not features:
            print("Features cannot be empty!")
            continue

        return [f.strip() for f in features.split(",") if f.strip()]


# main menu
def main():
    collection = connect_db()
    if not collection:
        return

    while True:
        print("\n--- MENU ---")
        print("1 - Add a cat")
        print("2 - Show all")
        print("3 - Find by name")
        print("4 - Update age")
        print("5 - Add feature")
        print("6 - Delete by name")
        print("7 - Delete all")
        print("0 - Exit")

        choice = input(">>> ")

        if choice == "1":
            create_cat(collection, input_name(), input_age(), input_features())

        elif choice == "2":
            read_all(collection)

        elif choice == "3":
            read_by_name(collection, input_name())

        elif choice == "4":
            update_age(collection, input_name(), input_age())

        elif choice == "5":
            add_feature(collection, input_name(), input_features())

        elif choice == "6":
            delete_by_name(collection, input_name())

        elif choice == "7":
            delete_all(collection)

        elif choice == "0":
            break


if __name__ == "__main__":
    main()