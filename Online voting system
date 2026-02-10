#1.Create a list of candidates
candidates = ["Amrutha", "Gautham", "Abhinav","Adithyan","Jacob"]

#2.Use a dictionary to store votes (Candidate → Vote Count)
votes = {candidate: 0 for candidate in candidates}
print("Welcome to the Online Voting System")
print("Candidates are:")
for candidate in candidates:
    print(candidate)
print("Type 'stop' to end voting\n")

#3.Accept votes from users and update the dictionary.
while True:
    vote = input("Enter candidate name to vote: ")

    if vote == "stop":
        break

# 5. Handle invalid candidate input
    elif vote in votes:
        votes[vote] += 1
        print("Vote recorded for", vote,"\n")
    else:
        print("Invalid candidate! Please try again.\n")

#4.Display total votes and announce the winner.
print("Voting Results")
for candidate in votes:
    print(candidate, ":", votes[candidate], "votes")

winner = ""
max_votes = 0

for candidate in votes:
    if votes[candidate] > max_votes:
        max_votes = votes[candidate]
        winner = candidate
print("--------")
print("Winner:", winner)
print("Votes:", max_votes)
