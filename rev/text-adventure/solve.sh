(
	echo "enter";
	echo "pick up torch";

	# Get the rope
	echo "go right";
	echo "cross the bridge";
	echo "take rope";
	echo "leave";
	echo "leave";

	# Get the sword
	echo "go center";
	echo "go down";
	echo "go right";
	echo "swing across";
	echo "take sword";
	echo "leave";
	echo "leave";
	echo "ascend";
	echo "leave";

	# Get the key
	echo "go left";
	echo "cut webs";
	echo "take key";
	echo "leave";
	echo "leave";

	# Win
	echo "go center";
	echo "go down";
	echo "go left";
	echo "unlock the door";
	echo "reach through the crack in the rocks";
	echo "the crack in the rocks concealing the magical orb with the flag";
) | nc challs.pwnoh.io 13376
