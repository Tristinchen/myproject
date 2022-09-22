<script>
var user = JSON.parse('{{ data | safe}}');
document.write(user)

<table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
  <tr>
    <td align="center" class="biaoti" height="60">库存统计报表</td>
  </tr>
  <tr>
    <td align="right" height="25">2022-09-20</td>
  </tr>
</table>

<table width="100%" border="0" cellspacing="1" cellpadding="4" bgcolor="#cccccc" class="tabtop13" align="center">
  <tr>
    <td class="btbg font-center titfont" rowspan="2">商品图片</td>
    <td width="10%" class="btbg font-center titfont" rowspan="2">商品标题</td>
    <td width="10%" class="btbg font-center titfont" rowspan="2">商品货号</td>
    <td width="10%" class="btbg font-center titfont" rowspan="2">商品品类</td>
    <td colspan="4" class="btbg font-center titfont">sku信息</td>
  </tr>
  <tr>
    <td width="8%" class="btbg2 font-center">颜色</td>
    <td width="8%" class="btbg2 font-center">尺码</td>
    <td width="8%" class="btbg2 font-center">sku code</td>
    <td width="8%" class="btbg2 font-center">库存</td>
  </tr>
<script>



cars = ({{data | tojson}})
for (var i=0,l=cars.length; i<l; i++){
    sku_num=cars[i]["sku_infos"];
    console.log(cars[i]);
<!--	sku_num=sku_num+1-->
    document.write('<tr>');
	document.write('<td width="10%" rowspan="'+ sku_num +'" class="btbg1 font-center"><img src=' + cars[i].img +'alt="Big Boat" width="120" height="150"></td>' );
	document.write('<td width="10%" rowspan="'+ sku_num +'" class="btbg1 font-center">' + cars[i].title +'</td>' );
	document.write('<td width="10%" rowspan="'+ sku_num +'" class="btbg1 font-center">' + cars[i].product_id +'</td>' );
	document.write('<td width="10%" rowspan="'+ sku_num +'" class="btbg1 font-center">DRESS</td>' );
	document.write('</tr>');
	for(var m=0, k=cars[i].color_infos.length; m<k; m++){
	    for (var n=0, l2=cars[i].color_infos[m].more.length; n<l2; n++){
	        for(var key in cars[i].color_infos[m].more[n]){
	            document.write('<tr>');
	            document.write('<td width="10%"  class="btbg1 font-center">' + cars[i].color_infos[m].color +'</td>');
	            document.write('<td width="8%"  class="btbg1 font-center">'+key+'</td>');
	            document.write('<td width="8%"  class="btbg1 font-center">'+cars[i].product_id+'-'+cars[i].color_infos[m].color+'-'+key+'</td>');
	            inventory=cars[i].color_infos[m].more[n][key].replace(/[^\d]/g," ");
	            document.write('<td width="8%"  class="btbg1 font-center ">'+inventory+'</td>');
	        }
	    }
	}

}
</table>

</script>