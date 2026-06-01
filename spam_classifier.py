from model import train_model


def main():
    stats = train_model()
    print("Model trained and saved successfully.")
    print(f"  Accuracy : {stats['accuracy']}%")
    print(f"  Samples  : {stats['samples']}")
    print(f"  Spam     : {stats['spam_count']}")
    print(f"  Ham      : {stats['ham_count']}")


if __name__ == "__main__":
    main()
