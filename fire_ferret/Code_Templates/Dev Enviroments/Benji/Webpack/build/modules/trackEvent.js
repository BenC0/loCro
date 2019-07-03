export default function trackEvent(label) {
	var tracker_exists = !!ga.getByName('cro_tracker') || false;

	if (!tracker_exists) {
		ga("create", 'UA-000000-0', { name: "cro_tracker" });
	}

	ga("cro_tracker.send", {
		hitType: "event",
		eventCategory: "CRO Test Reporting",
		eventAction: 'TE001',
		eventLabel: label
	});
	window.hj=window.hj||function(){(hj.q=hj.q||[]).push(arguments);};
	// Tag the recording with one or more tags...
	console.log(`Hotjar Trigger: TE001_${label.replace(' ', '_')}`)
	hj('trigger', [`TE001_${label.replace(' ', '_')}`]);
	hj('tagRecording', [`TE001_${label}`]);
}