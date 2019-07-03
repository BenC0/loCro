console.log('locro called')

function determine_desired_variant() {
	let urlParams = new URLSearchParams(window.location.search);
	let desired_variant = urlParams.get('variant');

	switch (desired_variant) {
		case null:
		case undefined:
		case "":
			return false
			break;
		default:
			return desired_variant
			break;
	}
}

function determine_filetype(file) {
	if (file.match(/.js$/g)) {
		return "js"
	} else if (file.match(/.css$/g)) {
		return "css"
	}
	return undefined
}

function load_variant(variant) {
	let filetype = determine_filetype(variant)
	let file_path = `/locro/${variant}`
	let asset_el;

	switch (filetype) {
		case "js":
			asset_el = document.createElement('script')
			asset_el.setAttribute('src',file_path)
			asset_el.setAttribute('type', 'text/javascript')
			document.head.appendChild(asset_el)
			break;
		case "css":
			asset_el = document.createElement('link')
			asset_el.setAttribute('href',file_path)
			asset_el.setAttribute('type', 'text/css')
			asset_el.setAttribute('rel', 'stylesheet')
			document.head.appendChild(asset_el)
			break;
	}
}

function locro_init() {
	let config_file_path = "/locro/config.json"
	fetch(config_file_path).then(response => {
		return response.json()
	}).then(config => {
		console.log(`config loaded`)

		let variations = config["variations"]
		
		let number_of_variations = variations.length
		if (number_of_variations === 0) {
			console.error('No variations detected. Please review your config file.');
		} else {
			console.log(`${number_of_variations} variations detected.`)
		}
		
		let desired_variant = determine_desired_variant()
		if (desired_variant === false) {
			console.error(`No variations selected. Please reload the page with the following query parameter:\n\n\t\t"variant=[variant_alias]"\n\n(replace [variant_alias] with the desired variant alias, which is defined in the config.json)`);
		} else {
			console.log(`Desired Variant: ${desired_variant}`)
		}

		for (var i = 0; i < number_of_variations; i++) {
			let v = variations[i]
			let aliases = v.aliases
			if (aliases.indexOf(desired_variant) !== -1) {
				desired_variant = v
			}
		}

		let variation_files =  desired_variant["files"]
		let variant_js = variation_files["js"] 
		let variant_css = variation_files["css"]

		if (variant_js === undefined && variant_css === undefined) {
			console.error(`No variation files declared. Please review your config file.`);
		} else {
			if (variant_js !== undefined) {
				console.log(`Variation js file: ${variant_js}`)
				load_variant(variant_js)
			}
			if (variant_css !== undefined) {
				console.log(`Variation css file: ${variant_css}`)
				load_variant(variant_css)
			}
		}
	})
}

locro_init()