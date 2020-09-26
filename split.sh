#/bin/sh
#
# install :  brew install glew glfw
# install : brew install ffmpeg $(brew options ffmpeg | grep -vE '\s' | grep -- '--with-' | tr '\n' ' ')

# cleanup
rm part*.MOV
rm tmp_part*.MOV

# split out files into parts based on input file input.txt in current directory
export IFS=" "
cat input.txt | while read a b c d; do ffmpeg -ss $b -i $a -t $c -c copy $d; done

## re-encode parts
for a in part*MOV; do ffmpeg -i $a tmp_$a ; done

## make highlight video
rm highlight.MOV
for f in ./tmp_part*.MOV; do echo "file '$f'" >> mylist.txt; done
ffmpeg -f concat -safe 0 -i mylist.txt -bsf:a aac_adtstoasc -fflags +genpts -c copy highlight.MOV
rm mylist.txt

## make goals video (all files with goal in the name)
rm goals.MOV
for f in ./tmp_part*goal*.MOV; do echo "file '$f'" >> mylist.txt; done
## ffmpeg -i input.jpg -vf "drawtext=text='Test Text':fontcolor=white:fontsize=75:x=1002:y=100:" output.jpg
#ffmpeg -i ../input.jpg -vf "drawtext=text='Goals':fontcolor=white:fontsize=75:x=1002:y=800:" output.jpg
#ffmpeg -f image2 -i output.jpg goalsintro.mov
## -filter_complex "gltransition=duration=4:offset=1.5"
ffmpeg -f concat -safe 0 -i mylist.txt -bsf:a aac_adtstoasc -fflags +genpts -c copy goals.MOV
rm mylist.txt

## ffmpeg -i input.jpg -vf "drawtext=text='Test Text':fontcolor=white:fontsize=75:x=1002:y=100:" output.jpg


