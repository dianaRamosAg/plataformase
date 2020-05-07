		function populate(selectM,selectL){
			var sm = document.getElementById(selectM);
			var sl = document.getElementById(selectL);
			

			sl.innerHTML = "";

			switch(sm.value){
				case 'Tepic':
					{%for element in localidadesTepic%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
					{%endfor%}
				break;

				case 'Acaponeta':
				{%for element in localidadesAcaponeta%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Ahuacatlán':
				{%for element in localidadesAhuacatlan%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Amatlán de Cañas':
				{%for element in localidadesAmatlan%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Compostela':
				{%for element in localidadesCompostela%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Huajicori':
				{%for element in localidadesHuajicori%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Ixtlán del Río':
				{%for element in localidadesIxtlan%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Jala':
				{%for element in localidadesJala%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Xalisco':
				{%for element in localidadesXalisco%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'El Nayar':
				{%for element in localidadesNayar%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Rosamorada':
				{%for element in localidadesRosamorada%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Ruíz':
				{%for element in localidadesRuiz%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'San Blas':
				{%for element in localidadesSanBlas%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'San Pedro Lagunillas':
				{%for element in localidadesSPL%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Santa María del Oro':
				{%for element in localidadesSMO%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Santiago Ixcuintla':
				{%for element in localidadesSantiago%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Tecuala':
				{%for element in localidadesTecuala%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Tuxpan':
				{%for element in localidadesTuxpan%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'La Yesca':
				{%for element in localidadesYesca%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;

				case 'Bahía de Banderas':
				{%for element in localidadesBahia%}
					var newOption = document.createElement("option");
					newOption.innerHTML = "{{element.Nombre}}";
					sl.options.add(newOption);
				{%endfor%}
				break;
			}

			
		
		}