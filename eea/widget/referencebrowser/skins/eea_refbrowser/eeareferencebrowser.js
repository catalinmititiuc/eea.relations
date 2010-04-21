var EEAReferenceBrowser = {version: '1.0.0'};

// Events
EEAReferenceBrowser.Events = function(){
  this.BASKET_ADD = 'EEA-REFERENCEBROWSER-BASKET-ADD';
  this.BASKET_DELETE = 'EEA-REFERENCEBROWSER-BASKET-DELETE';
  this.AJAX_START = 'EEA-REFERENCEBROWSER-AJAX-START';
  this.AJAX_STOP = 'EEA-REFERENCEBROWSER-AJAX-STOP';
  this.SAVE = 'EEA-REFERENCEBROWSER-SAVE';
  this.CANCEL = 'EEA-REFERENCEBROWSER-CANCEL';
  this.CLOSE = 'EEA-REFERENCEBROWSER-CLOSE';
  this.SAVED = 'EEA-REFERENCEBROWSER-SAVED';
};

EEAReferenceBrowser.Events.prototype = {};

EEAReferenceBrowser.Tab = function(context, parent){
  this.parent = parent;
  this.context = context;
  this.panel = jQuery(context.panel);
  this.tab = jQuery(context.tab);
  this.name = this.panel.attr('id');
  this.url = jQuery('.tab-url', this.tab).text();
  this.panel.height(parent.height - 180);
  this.panel.css('overflow', 'auto');

  var self = this;
  Faceted.Load(0, this.url + '/');
  jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(evt){
    self.setup_links();
  });
};

EEAReferenceBrowser.Tab.prototype = {
  get_icon: function(){
  return jQuery('<div>').addClass('ui-icon')
                        .addClass('ui-icon-extlink')
                        .addClass('ui-icon-custom-add');
  },

  setup_links: function(){
    var results = jQuery('#faceted-results', this.panel);
    this.folder_summary_view(results);
    this.tabular_view(results);
    this.album_view(results);
    this.folder_listing(results);
  },

  folder_summary_view: function(context){
    // Folder summary view
    var items = jQuery('.tileItem', context);
    jQuery('a', items).click(function(){
      return false;
    });

    // Add working css class
    items.addClass('refbrowser-faceted-addable-item');
    items.attr('title', 'Click to add it to current relations');
    items.prepend(this.get_icon());

    // Handle clicks
    var js_context = this;
    items.click(function(){
      var self = jQuery(this);
      self.effect('transfer', {to: '#' + js_context.parent.name + '-popup-selected-items'}, 'slow', function(){
        jQuery(js_context.parent.events).trigger(
          js_context.parent.events.BASKET_ADD,
          {url: jQuery('.tileHeadline a', self).attr('href')}
        );
      });
    });
  },

  tabular_view: function(context){
    // Tabular view
    var js_context = this;
    var table = jQuery('table', context);
    jQuery('a', table).click(function(){
      return false;
    });

    table.css('width', '100%');

    var th = jQuery('thead tr', table);
    th.append(jQuery('<th>').width(20));

    var rows = jQuery('tbody tr', table);
    rows.each(function(){
      var self = jQuery(this);
      self.attr('title', 'Click to add it to current relations');
      var td = jQuery('<td>');
      td.append(js_context.get_icon());
      self.append(td);
      // Backet add
      self.click(function(){
        self.effect('transfer', {to: '#' + js_context.parent.name + '-popup-selected-items'}, 'slow', function(){
          jQuery(js_context.parent.events).trigger(
            js_context.parent.events.BASKET_ADD,
            {url: jQuery('a', self).attr('href')}
          );
        });
      });
    });
    // Add working css class
    jQuery('tr', context).addClass('refbrowser-faceted-addable-item');
  },

  album_view: function(context){
    var js_context = this;
    var items = jQuery('.photoAlbumEntry', context);
    jQuery('a', items).click(function(){
      return false;
    });

    // Add working css class
    items.addClass('refbrowser-faceted-addable-item');
    items.attr('title', 'Click on right-top icon to add it to current relations');
    items.prepend(this.get_icon());

    items.click(function(){
      var self = jQuery(this);
      self.effect('transfer', {to: '#' + js_context.parent.name + '-popup-selected-items'}, 'slow', function(){
        jQuery(js_context.parent.events).trigger(
          js_context.parent.events.BASKET_ADD,
          {url: jQuery('a', self).attr('href')}
        );
      });
    });
  },

  folder_listing: function(context){
    // Folder listing
    var js_context = this;
    var items = jQuery('dt', context);
    jQuery('a', items).click(function(){
      return false;
    });

    items.addClass('refbrowser-faceted-addable-item');
    items.attr('title', 'Click to add it to current relations');
    items.prepend(this.get_icon());

    // Add working css class
    items.click(function(){
      var self = jQuery(this);
      self.effect('transfer', {to: '#' + js_context.parent.name + '-popup-selected-items'}, 'slow', function(){
        jQuery(js_context.parent.events).trigger(
          js_context.parent.events.BASKET_ADD,
          {url: jQuery('a', self).attr('href')}
        );
      });
    });
  }
};

EEAReferenceBrowser.Basket = function(context, parent){
  this.context = context;
  this.parent = parent;
  this.context.height(this.parent.height - 128);
  this.context.css('overflow', 'auto');
  jQuery('.tileItem', this.context).attr('title', 'Click and drag to change order');
  this.context.sortable({
    items: '.tileItem',
    placeholder: 'ui-state-highlight'
  });

  this.initialize();
  var self = this;

  // Basket add
  jQuery(self.parent.events).bind(self.parent.events.BASKET_ADD,
    function(evt, data){
      self.basket_add_clicked(data);
    }
  );

  // Working in background
  jQuery(self.parent.events).bind(self.parent.events.AJAX_START,
    function(evt, data){
      jQuery('h4', self.context).addClass('ui-state-working');
    }
  );
  jQuery(self.parent.events).bind(self.parent.events.AJAX_STOP,
    function(evt, data){
      jQuery('h4', self.context).removeClass('ui-state-working');
    }
  );

  // Save button clicked
  jQuery(self.parent.events).bind(self.parent.events.SAVE,
    function(evt, data){
      self.save();
    }
  );

  // Cancel button clicked
  jQuery(self.parent.events).bind(self.parent.events.CANCEL,
    function(evt, data){
      self.cancel();
    }
  );

  // Popup closed
  jQuery(self.parent.events).bind(self.parent.events.CLOSE,
    function(evt, data){
      self.close();
    }
  );
};

EEAReferenceBrowser.Basket.prototype = {
  initialize: function(){
    jQuery('.tileItem', this.context).prepend(this.trash_icon());
    jQuery('.ui-icon-basket-trash', this.context).click(function(){
      var self = jQuery(this);
      self.parent().slideUp(function(){
        jQuery(this).remove();
      });
    });
  },

  trash_icon: function(){
    return jQuery('<div>').addClass('ui-icon')
                               .addClass('ui-icon-trash')
                               .addClass('ui-icon-basket-trash')
                               .text('X');
  },

  get_url: function(url){
    var last_slash = url.lastIndexOf('/');
    var view = url.slice(last_slash+1, url.length);
    url = url.slice(0, last_slash);
    if(!view){
      return url;
    }
    // View
    if(view==='view'){
      return url;
    }
    // Zope 3 view
    if(view.indexOf('@@')===0){
      return url;
    }
    // index_html
    if(view.indexOf('index_html')!==-1){
      return url;
    }
    // index.html
    if(view.indexOf('index.html')!==-1){
      return url;
    }
    // Other view
    if(view.indexOf('_view')!==-1){
      return url;
    }
    return url + '/' + view;
  },

  basket_add_clicked: function(data){
    var url = this.get_url(data.url);
    var query = {};
    query.mode = 'edit';
    query.field = this.parent.name;
    query.nocache = new Date().getTime();
    var self = this;
    jQuery(self.parent.events).trigger(self.parent.events.AJAX_START);
    jQuery.get(url + '/@@eeareferencebrowser-popup-selecteditem.html', query, function(data){
      self.basket_add(data);
      jQuery(self.parent.events).trigger(self.parent.events.AJAX_STOP);
    });
  },

  basket_add: function(data){
    var data_dom = jQuery(data);
    var uid = jQuery('input[type=checkbox]', data_dom).val();
    var exists = jQuery('input[value=' + uid + ']', this.context);
    if(exists.length){
      var parent = exists.parent();
      parent.addClass('ui-pulsate-item');
      parent.effect('pulsate', {}, 200, function(){
        jQuery(this).removeClass('ui-pulsate-item');
      });
    }else{
      data_dom.prepend(this.trash_icon());
      jQuery('.ui-icon-basket-trash', data_dom).click(function(){
        var self = jQuery(this);
        self.parent().slideUp(function(){
          jQuery(this).remove();
        });
      });
      jQuery('.eea-ref-selecteditems', this.context).append(data_dom);
    }
  },

  save: function(){
    var self = this;
    var query = {};
    var values = jQuery('input[type=checkbox]', this.context);
    values = jQuery.map(values, function(input, i){
      return jQuery(input).val();
    });
    query.field = this.parent.name;
    query.nocache = new Date().getTime();
    query[this.parent.name] = values;
    var url = '@@eeareferencebrowser.save';
    jQuery(self.parent.events).trigger(self.parent.events.AJAX_START);
    jQuery.post(url, query, function(data){
      jQuery(self.parent.events).trigger(self.parent.events.AJAX_STOP);
      jQuery(self.parent.events).trigger(self.parent.events.SAVED, {msg: data});
    });
  },

  cancel: function(){
    return;
  },

  close: function(){
    var self = this;
    var url = '@@eeareferencebrowser-popup-selecteditems.html';
    var query = {};
    query.mode = 'edit';
    query.field = this.parent.name;
    query.nocache = new Date().getTime();

    jQuery.get(url, query, function(data){
      jQuery('.eea-ref-selecteditems', self.context).html(data);
      self.initialize();
    });
  }
};

EEAReferenceBrowser.Widget = function(name){
  this.name = name;
  this.context = jQuery('#' + name + "-widget");
  this.popup = jQuery('#' + name + '-popup', this.context);
  this.workspace = jQuery('.popup-tabs' , this.popup);
  this.basket = null;
  this.button = jQuery('input[type=button]', this.context);
  this.current_tab = null;

  this.events = new EEAReferenceBrowser.Events();
  this.width = jQuery(window).width() * 0.85;
  this.height = jQuery(window).height() * 0.95;
  var js_context = this;

  // Popup dialog
  this.popup.dialog({
    bgiframe: true,
    modal: true,
    closeOnEscape: false,
    autoOpen: false,
    width: js_context.width,
    height: js_context.height,
    resize: false,
    buttons: {
      'Save': function(){
        jQuery(js_context.events).trigger(js_context.events.SAVE);
      },
      'Cancel': function(){
        jQuery(js_context.events).trigger(js_context.events.CANCEL);
        jQuery(this).dialog('close');
      }
    },
    close: function(){
      jQuery(js_context.events).trigger(js_context.events.CLOSE);
    }
  });

  // Tabs
  this.workspace.tabs({
    select: function(event, ui){
      Faceted.Cleanup();
      jQuery('.popup-tabs #faceted-form').remove();
    },
    load: function(event, ui){
      js_context.tab_selected(ui);
    }
  });

  // Basket
  var basket = jQuery('.popup-selected-items', this.popup);
  this.basket = new EEAReferenceBrowser.Basket(basket, this);

  // Add button
  this.button.click(function(){
    scroll(0, 0);
    js_context.popup.dialog('open');
    jQuery(Faceted.Events).trigger(Faceted.Events.WINDOW_WIDTH_CHANGED);
  });

  jQuery(this.events).bind(this.events.SAVED, function(evt, data){
    js_context.saved(data);
  });
};

EEAReferenceBrowser.Widget.prototype = {
  tab_selected: function(ui){
    this.current_tab = new EEAReferenceBrowser.Tab(ui, this);
  },

  saved: function(data){
    var area = jQuery('.eea-ref-selecteditems-box', this.context.parent());
    if(area.length){
      var self = this;
      var url = '@@eeareferencebrowser-popup-selecteditems.html';
      var query = {};
      query.mode = 'view';
      query.field = self.name;
      query.nocache = new Date().getTime();

      jQuery.get(url, query, function(data){
        area.html(data);
      });
    }
    this.popup.dialog('close');
  }
};
