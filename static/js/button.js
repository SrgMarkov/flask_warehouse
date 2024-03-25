$('.quantity_inner .bt_minus').click(function() {
    let $input = $(this).parent().find('.quantity');
    let count = parseInt($input.val()) - 1;
    count = count < 0 ? 0 : count;
    $input.val(count);
    var id = $(this).attr("id");
	$.ajax({
        url: "/delete_count",
        type: "POST",
        contentType: "application/json",
        data: {"id": id},
    });
});

$('.quantity_inner .bt_plus').click(function() {
    let $input = $(this).parent().find('.quantity');
    let count = parseInt($input.val()) + 1;
    count = count > parseInt($input.data('max-count')) ? parseInt($input.data('max-count')) : count;
    $input.val(parseInt(count));
	var id = $(this).attr("id");
	$.ajax({
        url: "/add_count",
        type: "POST",
        contentType: "application/json",
        data: {"id": id},
    });
});

$('#quantity_asc').click(function() {
	var id = $(this).attr("id");
	$.ajax({
        url: "/",
        type: "POST",
        contentType: "application/json",
        data: {"id": id},
    });
});
