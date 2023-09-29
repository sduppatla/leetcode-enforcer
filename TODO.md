TODO:
* Deploy to actual server soon -- really just have to add cleanup tbh
* Add support for multiple different enforcements
    * /enforcement should be able to switch between these options on a per user basis
    * switching between limited role and user's current role (will require storing in db)
* Add the ability to set the threshold via discord as well (will need to store in db :>)
* Ensure that whenever bot is shut down user's are not restricted unfairly
    * Likely just add some cleanup command that undoes any applied modifications as this will be manually hosted for time being
* Adjust bot permissions to be more restrictive -- right now just fully administrative
* Add support for logging output to a specific channel
* Add bot commands to retrieve information from db to see currently applied enforcements + user data (nothing is sensitive)
* Eventually containerize and deploy somewhere else for fun :)
