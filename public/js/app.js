$(function(){
  $("a[method='delete']").click(function(){
    node = $(this)
    url = node.attr("href")
    console.log(node.attr("href"))
    $.ajax({
      url: url,
      type: "delete",
    }).done(function(data) {
      console.log(data)
    });
    return false
  });
})