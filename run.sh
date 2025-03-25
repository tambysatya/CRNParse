



MODELS=`ls models/biomodels/BIO*`

for MODEL in $MODELS
do
	NAME=`basename $MODEL .xml`
	TGT="output/$NAME.txt"

	if ! python main.py -i $MODEL -o $TGT; then
		echo "ERROR for $MODEL"	
		break
	fi
done

