import { fetchDB } from "../db/practice.js";

// User logout button: When the logout button is clicked, this will
// log the user out of the system.
const logoutButton = document.getElementById('logout')
logoutButton.addEventListener('click', async (logoutEvent) =>{
    logoutEvent.preventDefault()
    console.log("Logout button in navbar clicked!")

    try {
        // TODO: Insert function that clears out the currentUser from the database

        window.location.href = "./index.html#LoggedOut"
    }
    catch (error) {
        console.error("Error during logout:", error)
    }
})