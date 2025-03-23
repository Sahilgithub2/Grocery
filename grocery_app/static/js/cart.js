// document.addEventListener("DOMContentLoaded", function () {
//     fetch("/view_cart/")
//         .then(response => response.json())
//         .then(data => {
//             let cartContainer = document.getElementById("cart-container");
//             let emptyCart = document.getElementById("emptyCart");

            
//             if (data.error || data.cart_items.length === 0) {
//                 emptyCart.classList.remove("hidden");
//                 cartContainer.innerHTML = "";
//                 return;
//             }

//             emptyCart.classList.add("hidden");
//             cartContainer.innerHTML = "";

//             data.cart_items.forEach(item => {
//                 let productCard = document.createElement("div");
//                 productCard.classList.add("bg-white", "p-4", "rounded-lg", "shadow-md", "w-[224px]", "text-center", "product-card", "mx-auto");

//                 productCard.innerHTML = `
//                     <img src="${item.image_url}" alt="${item.product_name}" class="w-full h-32 object-cover rounded-md">
//                     <h3 class="text-lg font-semibold mt-2">${item.product_name}</h3>
//                     <p class="price font-bold">R ${item.price}</p>
//                     <p class="text-gray-700">Quantity: <span class="font-semibold">${item.quantity}</span></p>
//                     <button class="removeButton text-red-600 py-2 px-6 rounded-lg bg-red-100 border border-red-600 
//                         font-bold hover:bg-white focus:outline-none focus:ring-2 focus:ring-red-400 transition duration-300"
//                         data-product-id="${item.id}">REMOVE</button>
//                 `;
//                 cartContainer.appendChild(productCard);
//             });

//             document.querySelectorAll(".removeButton").forEach(button => {
//                 button.addEventListener("click", function () {
//                     let productId = this.getAttribute("data-product-id");

//                     console.log("🔹 Removing Product ID:", productId);  // Debugging

//                     removeFromCart(productId, this);
//                 });
//             });
//         })
//         .catch(error => console.error("Error fetching cart:", error));
// });
// function getCSRFToken() {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//         document.cookie.split(";").forEach(cookie => {
//             const [name, value] = cookie.trim().split("=");
//             if (name === "csrftoken") cookieValue = value;
//         });
//     }
//     return cookieValue;
// }


function removeFromCart(productId, buttonElement) {
    fetch("/remove_from_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            buttonElement.closest(".product-card").remove();
        } else {
            console.error("Error removing product:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}
document.addEventListener("DOMContentLoaded", function () {
    let cartContainer = document.getElementById("cart-container");
    let emptyCart = document.getElementById("emptyCart");

    // ✅ Prevent errors if the cart elements are missing
    if (!cartContainer || !emptyCart) {
        console.warn("🚨 cart-container or emptyCart is missing on this page. Skipping cart script.");
        return;
    }

    fetch("/view_cart/")
        .then(response => response.json())
        .then(data => {
            if (data.error || data.cart_items.length === 0) {
                emptyCart.classList.remove("hidden");
                cartContainer.innerHTML = "";
                return;
            }

            emptyCart.classList.add("hidden");
            cartContainer.innerHTML = "";

            data.cart_items.forEach(item => {
                let productCard = document.createElement("div");
                productCard.classList.add("bg-white", "p-4", "rounded-lg", "shadow-md", "w-[224px]", "text-center", "product-card", "mx-auto");

                productCard.innerHTML = `
                    <img src="${item.image_url}" alt="${item.product_name}" class="w-full h-32 object-cover rounded-md">
                    <h3 class="text-lg font-semibold mt-2">${item.product_name}</h3>
                    <p class="price font-bold">R ${item.price}</p>
                    <button class="removeButton text-red-600 py-2 px-6 rounded-lg bg-red-100 border border-red-600 
                        font-bold hover:bg-white focus:outline-none focus:ring-2 focus:ring-red-400 transition duration-300"
                        data-product-id="${item.id}">REMOVE</button>
                `;

                cartContainer.appendChild(productCard);
            });

            document.querySelectorAll(".removeButton").forEach(button => {
                button.addEventListener("click", function () {
                    let productId = this.getAttribute("data-product-id");
                    removeFromCart(productId, this);
                });
            });
        })
        .catch(error => console.error("❌ Error fetching cart:", error));
});

// ✅ Function to remove item from cart
function removeFromCart(productId, buttonElement) {
    fetch("/remove_from_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            buttonElement.closest(".product-card").remove();
        } else {
            console.error("❌ Error removing product:", data.error);
        }
    })
    .catch(error => console.error("❌ Error:", error));
}

// ✅ Function to get CSRF token
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            const [name, value] = cookie.trim().split("=");
            if (name === "csrftoken") cookieValue = value;
        });
    }
    return cookieValue;
}

