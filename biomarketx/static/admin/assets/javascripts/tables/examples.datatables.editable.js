/*
Name: 			Tables / Editable - Examples
Written by: 	Okler Themes - (http://www.okler.net)
Theme Version: 	1.5.1
*/

(function($) {

	'use strict';

	var EditableTable = {

		options: {
			addButton: '#addToTable',
			table: '#datatable-editable',
			dialog: {
				wrapper: '#dialog',
				cancelButton: '#dialogCancel',
				confirmButton: '#dialogConfirm',
			}
		},

		initialize: function() {
			this
				.setVars()
				.build()
				.events();
		},

		setVars: function() {
			this.$table				= $( this.options.table );
			this.$addButton			= $( this.options.addButton );

			// dialog
			this.dialog				= {};
			this.dialog.$wrapper	= $( this.options.dialog.wrapper );
			this.dialog.$cancel		= $( this.options.dialog.cancelButton );
			this.dialog.$confirm	= $( this.options.dialog.confirmButton );

			return this;
		},

		build: function() {
			this.datatable = this.$table.DataTable({
				/*aoColumns: [
					null,
					null,
					null,
					{ "bSortable": false }
				]*/
			});

			window.dt = this.datatable;

			return this;
		},

		events: function() {
			var _self = this;

			this.$table
				.on('click', 'a.save-row', function( e ) {
					e.preventDefault();

					_self.rowSave( $(this).closest( 'tr' ) );
				})
				.on('click', 'a.cancel-row', function( e ) {
					e.preventDefault();

					_self.rowCancel( $(this).closest( 'tr' ) );
				})
				.on('click', 'a.edit-row', function( e ) {
					e.preventDefault();

					_self.rowEdit( $(this).closest( 'tr' ) );
				})



				.on( 'click', 'a.remove-row1', function( e ) {
					e.preventDefault();
					//alert("f***")
					/*var user_id= $(this).attr("id")*/
					var $row = $(this).closest( 'tr' );
					var service_id= $(this).attr("id")
					//alert(service_id)

					$.magnificPopup.open({
						items: {
							src: _self.options.dialog.wrapper,
							type: 'inline'
						},
						preloader: false,
						modal: true,
						callbacks: {
							change: function() {
								_self.dialog.$confirm.on( 'click', function( e ) {
									e.preventDefault();
									//alert(user_id)
									// alert(user_id)
									// $.ajax({
									// 	type: "POST",
									// 	url: '/backend/users/del/'+user_id+'/',  // or just url: "/my-url/path/"
									// 	success: function() {
									// 		_self.rowRemove( $row );
									// 		$.magnificPopup.close();
									// 		alert("Congratulations!");
									// 		},
									// 	error: function() {
									// 		alert("Report error");
									// 		}
									// 	});
									$.ajax({
									    url: '/backend/service/del/'+service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         //alert(service_id)
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									}); 

									/*$.ajax({
									    url: '/backend/service/del/'+service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         alert("backend")
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									});*/


									//ajax call success
									
									//ajax call error
								});
							},
							close: function() {
								_self.dialog.$confirm.off( 'click' );
							}
						}
					});
				})




				.on( 'click', 'a.remove-row2', function( e ) {
					e.preventDefault();
					//alert("aiikjiui")
					/*var user_id= $(this).attr("id")*/
					var $row = $(this).closest( 'tr' );
					var sub_service_id= $(this).attr("id")
					//alert(sub_service_id)

					$.magnificPopup.open({
						items: {
							src: _self.options.dialog.wrapper,
							type: 'inline'
						},
						preloader: false,
						modal: true,
						callbacks: {
							change: function() {
								_self.dialog.$confirm.on( 'click', function( e ) {
									e.preventDefault();
									//alert(user_id)
									// alert(user_id)
									// $.ajax({
									// 	type: "POST",
									// 	url: '/backend/users/del/'+user_id+'/',  // or just url: "/my-url/path/"
									// 	success: function() {
									// 		_self.rowRemove( $row );
									// 		$.magnificPopup.close();
									// 		alert("Congratulations!");
									// 		},
									// 	error: function() {
									// 		alert("Report error");
									// 		}
									// 	});
									$.ajax({
									    url: '/backend/service/sub/del/'+sub_service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         //alert(sub_service_id)
									        _self.rowRemove( $row );
											$.magnificPopup.close();
											//window.location = '/backend/services/';

									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									}); 

									/*$.ajax({
									    url: '/backend/service/del/'+service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         alert("backend")
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									});*/


									//ajax call success
									
									//ajax call error
								});
							},
							close: function() {
								_self.dialog.$confirm.off( 'click' );
							}
						}
					});
				})


				.on( 'click', 'a.remove-row-lab-service', function( e ) {
					e.preventDefault();
					// alert("f***")
					var lab_service_id= $(this).attr("id")
					var $row = $(this).closest( 'tr' );
					//var service_id= $(this).attr("id")
					console.log(lab_service_id)
					//alert(lab_service_id)

					$.magnificPopup.open({
						items: {
							src: _self.options.dialog.wrapper,
							type: 'inline'
						},
						preloader: false,
						modal: true,
						callbacks: {
							change: function() {
								_self.dialog.$confirm.on( 'click', function( e ) {
									e.preventDefault();
									
									$.ajax({
									    url: '/provider/lab-service/del/'+lab_service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									    	//alert(lab_service_id)
									         //alert(user_id)
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									}); 

									
								});
							},
							close: function() {
								_self.dialog.$confirm.off( 'click' );
							}
						}
					});
				})

				.on( 'click', 'a.remove-row', function( e ) {
					e.preventDefault();
					// alert("f***")
					var user_id= $(this).attr("id")
					var $row = $(this).closest( 'tr' );
					var service_id= $(this).attr("id")
					//alert(service_id)

					$.magnificPopup.open({
						items: {
							src: _self.options.dialog.wrapper,
							type: 'inline'
						},
						preloader: false,
						modal: true,
						callbacks: {
							change: function() {
								_self.dialog.$confirm.on( 'click', function( e ) {
									e.preventDefault();
									//alert(user_id)
									// alert(user_id)
									// $.ajax({
									// 	type: "POST",
									// 	url: '/backend/users/del/'+user_id+'/',  // or just url: "/my-url/path/"
									// 	success: function() {
									// 		_self.rowRemove( $row );
									// 		$.magnificPopup.close();
									// 		alert("Congratulations!");
									// 		},
									// 	error: function() {
									// 		alert("Report error");
									// 		}
									// 	});
									$.ajax({
									    url: '/backend/users/del/'+user_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         //alert(user_id)
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									}); 

									/*$.ajax({
									    url: '/backend/service/del/'+service_id+'/',
									    type: 'get', // This is the default though, you don't actually need to always mention it
									    success: function() {
									         alert("backend")
									        _self.rowRemove( $row );
											$.magnificPopup.close();
									    },
									    error: function() { 
									        alert('Got an error dude');
									    }
									});*/


									//ajax call success
									
									//ajax call error
								});
							},
							close: function() {
								_self.dialog.$confirm.off( 'click' );
							}
						}
					});
				});

			this.$addButton.on( 'click', function(e) {
				e.preventDefault();

				_self.rowAdd();
			});

			this.dialog.$cancel.on( 'click', function( e ) {
				e.preventDefault();
				$.magnificPopup.close();
			});

			return this;
		},

		// ==========================================================================================
		// ROW FUNCTIONS
		// ==========================================================================================
		rowAdd: function() {
			this.$addButton.attr({ 'disabled': 'disabled' });

			var actions,
				data,
				$row;

			actions = [
				'<a href="#" class="hidden on-editing save-row"><i class="fa fa-save"></i></a>',
				'<a href="#" class="hidden on-editing cancel-row"><i class="fa fa-times"></i></a>',
				'<a href="#" class="on-default edit-row"><i class="fa fa-pencil"></i></a>',
				'<a href="#" class="on-default remove-row"><i class="fa fa-trash-o"></i></a>'
			].join(' ');

			data = this.datatable.row.add([ '', '', '', actions ]);
			$row = this.datatable.row( data[0] ).nodes().to$();

			$row
				.addClass( 'adding' )
				.find( 'td:last' )
				.addClass( 'actions' );

			this.rowEdit( $row );

			this.datatable.order([0,'asc']).draw(); // always show fields
		},

		rowCancel: function( $row ) {
			var _self = this,
				$actions,
				i,
				data;

			if ( $row.hasClass('adding') ) {
				this.rowRemove( $row );
			} else {

				data = this.datatable.row( $row.get(0) ).data();
				this.datatable.row( $row.get(0) ).data( data );

				$actions = $row.find('td.actions');
				if ( $actions.get(0) ) {
					this.rowSetActionsDefault( $row );
				}

				this.datatable.draw();
			}
		},

		rowEdit: function( $row ) {
			var _self = this,
				data;

			data = this.datatable.row( $row.get(0) ).data();

			$row.children( 'td' ).each(function( i ) {
				var $this = $( this );

				if ( $this.hasClass('actions') ) {
					_self.rowSetActionsEditing( $row );
				} else {
					$this.html( '<input type="text" class="form-control input-block" value="' + data[i] + '"/>' );
				}
			});
		},

		rowSave: function( $row ) {
			var _self     = this,
				$actions,
				values    = [];

			if ( $row.hasClass( 'adding' ) ) {
				this.$addButton.removeAttr( 'disabled' );
				$row.removeClass( 'adding' );
			}

			values = $row.find('td').map(function() {
				var $this = $(this);

				if ( $this.hasClass('actions') ) {
					_self.rowSetActionsDefault( $row );
					return _self.datatable.cell( this ).data();
				} else {
					return $.trim( $this.find('input').val() );
				}
			});

			this.datatable.row( $row.get(0) ).data( values );

			$actions = $row.find('td.actions');
			if ( $actions.get(0) ) {
				this.rowSetActionsDefault( $row );
			}

			this.datatable.draw();
		},

		rowRemove: function( $row ) {
			if ( $row.hasClass('adding') ) {
				alert("row remove")
				this.$addButton.removeAttr( 'disabled' );
			}
			//$(".on-default remove-row").val()
			//$this.hasClass("on-default remove-row").val()
			
			// alert($row[0])
			// return (backend/del_users)
			this.datatable.row( $row.get(0) ).remove().draw();
		},

		rowSetActionsEditing: function( $row ) {
			$row.find( '.on-editing' ).removeClass( 'hidden' );
			$row.find( '.on-default' ).addClass( 'hidden' );
		},

		rowSetActionsDefault: function( $row ) {
			$row.find( '.on-editing' ).addClass( 'hidden' );
			$row.find( '.on-default' ).removeClass( 'hidden' );
		}

	};

	$(function() {
		EditableTable.initialize();
	});

}).apply(this, [jQuery]);
			//alert($(".dataTables_length").html())

