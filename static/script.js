/* Write Javascript (using axios and jQuery) that:
• queries the API to get the cupcakes and adds to the page
• handles form submission to both let the API know about the new cupcake and updates the list on the page to show it. */


function addHTML(cupcake) {
    return `
        <div cupcake-info=${cupcake.id}>
        <li>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class="delete-button">X</button>
        </li>
        <img class="cupcake-img"
                src="${cupcake.image}">
        </div>`;
}


async function showCupcakeGallery() {
    const response = await axios.get(`http://localhost:5000/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(addHTML(cupcakeData));
        $("#cupcake-gallery").append(newCupcake);
    }
}


$("#add-cupcake-form").on("submit", async function (event) {
    event.preventDefault();

    try {
        let flavor = $("#form-flavor").val();
        let rating = $("#form-rating").val();
        let size = $("#form-size").val();
        let image = $("#form-image").val();

        const newCupcakeResponse = await axios.post(`http://localhost:5000/cupcakes`, { flavor, rating, size, image });

        let newCupcake = $(addHTML(newCupcakeResponse.data.cupcake));
        $("#cupcake-gallery").append(newCupcake);
        $("#add-cupcake-form").trigger("reset");
    } catch (error) {
        console.error("There was a problem adding the cupcake:", error);
    }
});


$("#cupcake-gallery").on("click", ".delete-button", async function (event) {
    event.preventDefault();
    let $cupcake = $(event.target).closest("div");
    let cupcakeId = $cupcake.attr("cupcake-info");

    await axios.delete(`http://localhost:5000/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showCupcakeGallery);