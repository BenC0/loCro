export function label_element(selector, label) {
	$(selector).attr('ip_id', label)
}

export function move_element(selector, method, target) {
	switch (method) {
		case "after":
			$(selector).insertAfter(target)
			break;
		case "before":
			$(selector).insertBefore(target)
			break;
		case "append":
			$(selector).appendTo(target)
			break;
		case "prepend":
			$(selector).prependTo(target)
			break;
	}
}

export function scroll_to(target, duration = 350) {
	if ($(target).length !== 0) {
		$('html, body').animate({
			scrollTop: $(target).offset().top
		}, duration)
	} else {
		console.warn(`Element doesn't exist: ${target}`)
	}
}

export function date_nth(d) {
	if (d > 3 && d < 21) return 'th'; 
	switch (d % 10) {
		case 1:  return "st";
		case 2:  return "nd";
		case 3:  return "rd";
		default: return "th";
	}
}

export function capitalise(str) {
	return str[0].toUpperCase() + str.toLowerCase().replace(/^./g, '')
}