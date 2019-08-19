$(document).ready(function () {
    var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};
    var brand=getUrlParameter('brand').replace('+',' ');
    var category=getUrlParameter('category').replace('+',' ');
    console.log(brand);
    console.log(category);
    $('#id_brand_select').val(brand);
    $('#id_category_select').val(category);
});