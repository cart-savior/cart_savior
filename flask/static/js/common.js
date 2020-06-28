// 모달창
function modal(){
	var btn_modal = document.querySelector("#btn_modal");
	if (btn_modal) {
		btn_modal.addEventListener("click", e => {
			document.querySelector("#modal_content").classList.remove("hide");
		})
	}
	var btn_close = document.querySelector("#btn_close");
	if (btn_close) {
		btn_close.addEventListener("click", e => {
			document.querySelector("#modal_content").classList.add("hide");
		})
	}
}

// 검색 버튼 및 키워드를 클릭했을 때 로딩하는 함수.
function loading(){
	var btn_search = document.querySelectorAll(".btn_search"),
		btn_other = document.querySelectorAll(".hash_item, #btn_more"),
		input = document.querySelectorAll(".inp_search");
	btn_search.forEach(item => {
		item.addEventListener("click", e => {
			input.forEach(item => {
				if (item.value.length != 0)
				{
					document.body.style.height = '100vh';
					document.body.style.position = 'fixed';
					document.body.style.overflow = 'hidden';
					document.getElementById("bg").style.display = "block";
					document.getElementById("loader").style.display = "flex";
				}
			})
		})
	});
	btn_other.forEach(item => {
		item.addEventListener("click", e => {
			document.body.style.height = '100vh';
			document.body.style.position = 'fixed';
			document.body.style.overflow = 'hidden';
			document.getElementById("bg").style.display = "block";
			document.getElementById("loader").style.display = "flex";
		})
	});
};
loading();
modal();

// 화면 사이즈를 확인하고 크기에 맞는 값을 리턴하는 함수
function change_value_by_media(pc, mobile) {
	var mql = window.matchMedia("screen and (max-width: 768px)");
	if (mql.matches) {
		return mobile;
	} else {
		return pc;
	}
}


