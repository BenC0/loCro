import "./v1.scss"
import { pollFor } from 'icarus';
import trackCampaign from './modules/trackCampaign';
import trackEvent from './modules/trackEvent';

import * as ip from "./modules/lib.js"

function init() {
	if (!$('body').hasClass('variant_loaded')) {
		$('body').addClass('variant_loaded')
	}
}

pollFor(function() {
	return typeof ga !== "undefined" && ga.loaded == true && typeof $ !== "undefined"
}, function() {
	init()
	trackCampaign('Variation 1');
});