// const loginForm = document.getElementById("loginForm");
// loginForm.addEventListener('submit', async (event) => {
//     event.preventDefault();
//     let email = document.getElementById("email").value;
//     let password = document.getElementById("password").value;


// });




// // Imports necessary for the login including some database functions
// // for validating credentials, and crytpography of passwords
// // @author Scott Ledford
// // import { fetchDB } from "../db/practice.js";
// // const key = "b6Sye6fN"

// // Handles the login credentials by grabbing the entered information and validating
// // then redirecting to website when finished validating
// // @author Scott Ledford
// const loginForm = document.getElementById("loginForm");
// loginForm.addEventListener('submit', async (event) => {
//     event.preventDefault();

//     let email = document.getElementById("email").value;
//     let password = document.getElementById("password").value;

//     try {
//         // Fetch the database
//         let data = await fetchDB();

//         // Check if the user exists and credentials match
//         let user = data.accounts.find(account => account.email === email && account.password === password);

//         if (user) {
//             // Set the current user in the database
//             data.currentUser.user = email;
//             // Redirect or perform further actions as needed
//             window.location.href = "../homePage.html#CredentialsValidated!Welcome_" + email;
//             console.log("User logged in:", data.currentUser)
//         } else {
//             console.log('Invalid credentials. Please try again.');
//         }
//     } catch (error) {
//         console.error("Error occurred:", error);
//     }
// });