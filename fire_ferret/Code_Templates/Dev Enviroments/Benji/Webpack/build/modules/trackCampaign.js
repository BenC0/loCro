export default function trackCampaign(variation, cd) {
	window.hj=window.hj||function(){(hj.q=hj.q||[]).push(arguments);};
	// Tag the recording with one or more tags...
	hj('trigger', [`TE001_${variation.replace(' ', '_')}`]);
	hj('tagRecording', [`TE001_${variation}`]);
	console.log(`TE001_${variation.replace(' ', '_')}`)
}

