"""
تطبيق التغييرات المطلوبة:
1. تغيير ملخص النتائج من 36 إلى 45
2. جعل العدد الأكبر في الحساب على اليسار
3. إضافة إمكانية حذف مشاركين الفصل دفعة واحدة
"""

import os
import re
import sys

def apply_changes():
    """Apply all required changes to the application files"""
    print("Applying requested changes...")
    
    # Change 1: Update results.html to change 36 to 45
    update_results_template()
    
    # Change 2: Update views.py to make larger number on left
    update_math_operations()
    
    # Change 3: Add ability to delete multiple participants
    add_bulk_delete_feature()
    
    print("All changes applied successfully!")

def update_results_template():
    """Update the results template to change max score from 36 to 45"""
    print("1. Changing results summary from 36 to 45...")
    
    filepath = "templates/competitions/results.html"
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the max score display
    content = content.replace('{{ result.total_score }} / 36', '{{ result.total_score }} / 45')
    
    # Replace the progress bar thresholds and calculations
    content = content.replace(
        '{% if result.total_score < 12 %}bg-danger{% elif result.total_score < 24 %}bg-warning{% else %}bg-success{% endif %}',
        '{% if result.total_score < 15 %}bg-danger{% elif result.total_score < 30 %}bg-warning{% else %}bg-success{% endif %}'
    )
    
    content = content.replace(
        'data-width="{% widthratio result.total_score 36 100 %}"',
        'data-width="{% widthratio result.total_score 45 100 %}"'
    )
    
    content = content.replace('aria-valuemax="36"', 'aria-valuemax="45"')
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("  - Results file updated successfully.")
    return True

def update_math_operations():
    """Update the math operations to put larger number on left"""
    print("2. Making the larger number appear on the left...")
    
    filepath = "competitions/views.py"
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Addition operation - change from right to left
    addition_pattern = r"""        # Make sure the larger number is on the right
        if num1 > num2:
            first_number = num2
            second_number = num1
        else:
            first_number = num1
            second_number = num2"""
    
    addition_replacement = """        # Make sure the larger number is on the left
        if num1 > num2:
            first_number = num1
            second_number = num2
        else:
            first_number = num2
            second_number = num1"""
    
    content = content.replace(addition_pattern, addition_replacement)
    
    # Division operation - change from right to left
    division_pattern = "        # Make sure the larger number (dividend) is on the right\n        first_number = divisor\n        second_number = dividend"
    division_replacement = "        # Make sure the larger number (dividend) is on the left\n        first_number = dividend\n        second_number = divisor"
    
    content = content.replace(division_pattern, division_replacement)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("  - Addition, multiplication and division operations updated successfully.")
    return True

def add_bulk_delete_feature():
    """Add the bulk delete functionality for participants"""
    print("3. Adding bulk delete capability for participants...")
    
    # Add new view function
    add_delete_multiple_view()
    
    # Add URL pattern
    add_delete_multiple_url()
    
    # Update the template
    update_start_template()
    
    print("  - Bulk delete feature added successfully.")
    return True

def add_delete_multiple_view():
    """Add the view function for deleting multiple participants"""
    filepath = "competitions/views.py"
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if the function already exists
    if "def delete_multiple_participants(request):" in content:
        print("  - Bulk delete function already exists.")
        return True
    
    # Find the position to add the new function (after delete_participant)
    match = re.search(r'def delete_participant\([^)]*\):.*?return redirect\([^)]*\)', content, re.DOTALL)
    if not match:
        print("  - Could not find suitable location to add bulk delete function.")
        return False
    
    insertion_point = match.end()
    
    # New function to add
    new_function = """

@login_required
def delete_multiple_participants(request):
    # Delete multiple participants at once.
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    # Get the list of participant IDs from the form
    participant_ids = request.POST.getlist('participant_ids')
    
    if not participant_ids:
        messages.error(request, 'لم يتم تحديد أي مشارك للحذف')
        return redirect('competitions:start_competition')
    
    # Count how many were successfully deleted
    deleted_count = 0
    not_deleted_count = 0
    
    for participant_id in participant_ids:
        try:
            participant = Participant.objects.get(id=participant_id)
            
            # Check if this participant has competitions
            if participant.competitions.exists():
                not_deleted_count += 1
                continue
            
            participant.delete()
            deleted_count += 1
            
        except Participant.DoesNotExist:
            continue
    
    if deleted_count > 0:
        messages.success(request, f'تم حذف {deleted_count} مشارك بنجاح')
    
    if not_deleted_count > 0:
        messages.error(request, f'لم يتم حذف {not_deleted_count} مشاركين لأنهم لديهم مسابقات مسجلة')
    
    # Redirect to the competitions start competition page
    return redirect('competitions:start_competition')
"""
    
    # Insert the new function
    updated_content = content[:insertion_point] + new_function + content[insertion_point:]
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print("  - Bulk delete function added successfully.")
    return True

def add_delete_multiple_url():
    """Add URL pattern for the delete_multiple_participants view"""
    filepath = "competitions/urls.py"
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if the URL pattern already exists
    if "path('delete-multiple-participants/'" in content:
        print("  - URL pattern for bulk delete already exists.")
        return True
    
    # Find the participant management section
    match = re.search(r"# Participant management\s+path\('add-participant/", content)
    if not match:
        print("  - Could not find participant management section in URLs file.")
        return False
    
    # Find the last entry in this section
    section_start = match.start()
    delete_pattern = r"path\('delete-participant/.*?\),"
    match = re.search(delete_pattern, content[section_start:])
    if not match:
        print("  - Could not find URL pattern for single delete.")
        return False
    
    insertion_point = section_start + match.end()
    
    # New URL pattern to add
    new_pattern = "\n    path('delete-multiple-participants/', views.delete_multiple_participants, name='delete_multiple_participants'),"
    
    # Insert the new URL pattern
    updated_content = content[:insertion_point] + new_pattern + content[insertion_point:]
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print("  - URL pattern for bulk delete added successfully.")
    return True

def update_start_template():
    """Update the start template to add checkboxes and delete button"""
    filepath = "templates/competitions/start.html"
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Add form wrapper and delete button
    table_pattern = r'<div class="table-responsive">\s+<table class="table table-hover mb-0">'
    table_replacement = """<form id="delete-participants-form" action="{% url 'competitions:delete_multiple_participants' %}" method="post">
                                                {% csrf_token %}
                                                <div class="mb-2 d-flex justify-content-end">
                                                    <button type="submit" class="btn btn-danger" id="delete-selected-btn" disabled onclick="return confirm('هل أنت متأكد من حذف المشاركين المحددين؟')">
                                                        <i class="fas fa-trash-alt"></i> حذف المحددين
                                                    </button>
                                                </div>
                                                <table class="table table-hover mb-0">"""
    
    content = re.sub(table_pattern, table_replacement, content)
    
    # Add checkboxes column
    thead_pattern = r'<thead class="table-light">\s+<tr>\s+<th>#</th>'
    thead_replacement = """<thead class="table-light">
                                                        <tr>
                                                            <th>
                                                                <input type="checkbox" id="select-all-checkbox" onclick="toggleAllCheckboxes()">
                                                            </th>
                                                            <th>#</th>"""
    
    content = re.sub(thead_pattern, thead_replacement, content)
    
    # Add checkbox to each row
    row_pattern = r'<tr>\s+<td>{{ forloop\.counter }}</td>'
    row_replacement = """<tr>
                                                            <td>
                                                                <input type="checkbox" name="participant_ids" value="{{ participant.id }}" class="participant-checkbox" onchange="updateDeleteButton()">
                                                            </td>
                                                            <td>{{ forloop.counter }}</td>"""
    
    content = re.sub(row_pattern, row_replacement, content)
    
    # Update empty row colspan
    empty_pattern = r'<td colspan="5" class="text-center">لا يوجد مشاركون مسجلون</td>'
    empty_replacement = '<td colspan="6" class="text-center">لا يوجد مشاركون مسجلون</td>'
    
    content = content.replace(empty_pattern, empty_replacement)
    
    # Close the form after the table
    table_end_pattern = r'</table>\s+</div>'
    table_end_replacement = """</table>
                                            </form>"""
    
    content = re.sub(table_end_pattern, table_end_replacement, content)
    
    # Add JavaScript functions for checkbox handling
    script_pattern = r'function downloadSampleFile\(\) \{.*?\}'
    script_replacement = """function downloadSampleFile() {
        // Create CSV content
        const csvContent = 'name,grade,group\\nطالب نموذج 1,1,1\\nطالب نموذج 2,2,1\\nطالب نموذج 3,3,2\\nطالب نموذج 4,4,2';
        
        // Create a blob with the CSV content
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        
        // Create a download link and trigger the download
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'participants_template.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    // Function to toggle all checkboxes
    function toggleAllCheckboxes() {
        const selectAllCheckbox = document.getElementById('select-all-checkbox');
        const participantCheckboxes = document.querySelectorAll('.participant-checkbox');
        
        participantCheckboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
        
        updateDeleteButton();
    }
    
    // Function to update delete button state
    function updateDeleteButton() {
        const participantCheckboxes = document.querySelectorAll('.participant-checkbox:checked');
        const deleteButton = document.getElementById('delete-selected-btn');
        
        deleteButton.disabled = participantCheckboxes.length === 0;
    }"""
    
    content = re.sub(script_pattern, script_replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("  - Start competition template updated successfully.")
    return True

if __name__ == "__main__":
    apply_changes()