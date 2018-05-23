from flask import jsonify

def help_msg():
	return jsonify(
			text = "Help for CSH Quotefault bot.\n"
			+ "All commands are in the form `/quote command_name [data and arguements]`\n\n"
			+ "`help` - displays this message\n"
			+ "`random` - grabs a random quote and posts it to the current channel",
			response_type="ephemeral"
			)
