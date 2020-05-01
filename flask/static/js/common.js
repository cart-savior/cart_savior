var btns = document.querySelectorAll(".btn_search, .hash_item");
btns.forEach(item => {
	item.addEventListener("click", e => {
		document.body.style.position = 'fixed';
		document.body.style.overflow = 'hidden';
		document.getElementById("bg").style.display = "block";
		document.getElementById("loader").style.display = "block";
	})
});
