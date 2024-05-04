  $(document).ready(function(){
    // Show or hide entries based on button click
    $('#loadMoreBtn').on('click', function() {
      $('.accordion-item.d-none').slice(0, 10).removeClass('d-none');
      if ($('.accordion-item.d-none').length === 0) {
        $(this).hide(); // Hide button when all entries are shown
      }
    });

    // Initialize, hide entries more than 10
    $('.accordion-item:gt(9)').addClass('d-none');

    $('.accordion-collapse').on('shown.bs.collapse', function () {
      $(this).prev().find('.accordion-button').addClass('active');
    });

    $('.accordion-collapse').on('hidden.bs.collapse', function () {
      $(this).prev().find('.accordion-button').removeClass('active');
    });

    // Log entry row-expand event
    $('.entry-row').click(function() {
      // Get entry ID 
      let entryId = $(this).data('entry-id');
      let clickedCategory = $(this).data('category');
      
      // Send AJAX request to log the event
      $.ajax({
          url: '/log_entry_click/',
          type: 'POST',
          data: {
              entry_id: entryId,
              clicked_category: clickedCategory,
              csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          success: function(data) {
              console.log('Event logged successfully');
          },
          error: function(xhr, status, error) {
              console.error('Error logging event:', error);
          }
      });
  });
  });
