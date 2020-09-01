function showpop(){
    data = document.getElementById('a1');
    data.style.display='block'
    $('[data-toggle="popover"]').popover('update')
}

$(function () {
    $('[data-toggle="popover"]').popover({
        trigger:"focus",
        placement:"bottom",
        container:"body",
        html:true,
        title:"Notificaciones",
        content: $('#a1'),
        boundary: "scrollParent"});
});