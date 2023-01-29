class A:

    def __call__(self):
        print("Call an object like a function")

class Pipeline:

    def __call__(self):
        print("You are using a pipeline, just like using a function.")


if __name__ == "__main__":
    a = A()
    a()

    pipeline = Pipeline()
    pipeline()