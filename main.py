from retriever import Retriever
from time import sleep


url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"

retriever = Retriever()
retriever.fetch(url=url)

# Now to visually "see" how much an asynchronous process is, we will render some numbers
for i in range(10):
    print("Waiting", 10-i)
    sleep(.3)  # Just to give it some time to finish if needed

while retriever._is_busy:
    print(".")
    sleep(.3)  # Just to give it some time to finish if needed

print("Thank you for your time. Process completed")
