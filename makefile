upload:
	rsync -av -e ssh --exclude=".git" ../comfy-image-nodes	flux:/home/ubuntu/ComfyUI/custom_nodes