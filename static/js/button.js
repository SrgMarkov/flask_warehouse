$('.quantity_inner .bt_minus').click(function() {
    let $input = $(this).parent().find('.quantity');
    let count = parseInt($input.val()) - 1;
    count = count < 0 ? 0 : count;
    $input.val(count);
    let id = $(this).attr("id");
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
	let id = $(this).attr("id");
	$.ajax({
        url: "/add_count",
        type: "POST",
        contentType: "application/json",
        data: {"id": id},
    });
});

$('.quantity_inner .bt_delete').click(function() {
	let id = $(this).attr("id");
	$.ajax({
        url: "/delete_product",
        type: "POST",
        contentType: "application/json",
        data: {"id": id},
    });
    location.reload()
});
