import json
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i')
	parser.add_argument('-o')
	args = parser.parse_args()

	print(args.i)

	dict_f = open("../../english_german.json")
	dict_ = json.load(dict_f)
	dict_f.close()

	with open("../../data/input.txt") as f:
		lines = f.readlines()

	translation = []
	for l in lines:
		words = []
		for w in l.split(" "):
			if w in dict_:
			    words.append(dict_[w])
			else:
			    words.append("tykva")
		translation.append(" ".join(words))

	with open("../../output_2.txt", "w") as f:
		f.write("\n".join(translation))
