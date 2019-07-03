import { pollFor } from 'icarus';
import trackCampaign from './modules/trackCampaign';

pollFor(function() {
	return typeof ga !== "undefined" && ga.loaded == true && typeof $ !== "undefined"
}, function() {
	trackCampaign('Control', '1');
});