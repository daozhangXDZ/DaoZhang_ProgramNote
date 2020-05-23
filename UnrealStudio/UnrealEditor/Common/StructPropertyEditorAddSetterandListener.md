# Custom Struct Property Editor Add Setter and Listener

2019年3月5日

15:59

 

**[HELP] Custom Struct Property Editor Add Setter and Listener**

08-01-2017, 06:26 AM

I have been struggling with this for a while and would really appreciate some guidance.

 

The goal is to create a dropdown list/combo box that contains strings that the user can select in the editor. This is to extend details customization.

 

I have created a custom structure like so.

 

Code:

USTRUCT()
     struct FTaskComponentData
     {
             GENERATED_BODY()
     
             UPROPERTY(VisibleAnywhere)
             TArray<FString>                                                                                                Names;
     
     };

Then I have created a class to implement the IPropertyTypeCustomization like so: 

(Header file):

 

Code:

class FTaskComponentDataCustomization : public IPropertyTypeCustomization
     {
     public:
             static TSharedRef<IPropertyTypeCustomization> MakeInstance();
      
             /** IPropertyTypeCustomization interface */
             virtual void CustomizeHeader(TSharedRef<class IPropertyHandle> StructPropertyHandle, class FDetailWidgetRow& HeaderRow, IPropertyTypeCustomizationUtils& StructCustomizationUtils) override;
             virtual void CustomizeChildren(TSharedRef<class IPropertyHandle> StructPropertyHandle, class IDetailChildrenBuilder& StructBuilder, IPropertyTypeCustomizationUtils& StructCustomizationUtils) override;
      
     private:
             TSharedPtr<IPropertyHandle> UPropertyTaskNameHandle;
     
             /** Visibility delegate for the various methods of calculating magnitude */
             EVisibility GetPropertyVisibility(UProperty* InProperty) const;
     };

(Source file):

 

Code:

TSharedRef<IPropertyTypeCustomization> FTaskComponentDataCustomization::MakeInstance()
     {
             return MakeShareable(new FTaskComponentDataCustomization());
     }
      
     void FTaskComponentDataCustomization::CustomizeHeader(TSharedRef<class IPropertyHandle> StructPropertyHandle, class FDetailWidgetRow& HeaderRow, IPropertyTypeCustomizationUtils& StructCustomizationUtils)
     {
             uint32 NumChildren;
             StructPropertyHandle->GetNumChildren(NumChildren);
      
             for (uint32 ChildIndex = 0; ChildIndex < NumChildren; ++ChildIndex)
             {
                     const TSharedRef< IPropertyHandle > ChildHandle = StructPropertyHandle->GetChildHandle(ChildIndex).ToSharedRef();
      
                     if (ChildHandle->GetProperty()->GetName() == TEXT("Names"))
                     {
                             UPropertyTaskNameHandle = ChildHandle;
                     }
             }
      
             check(UPropertyTaskNameHandle.IsValid());
     
     
             static TArray< TSharedPtr<FString>> something;
     
             something.Add(TSharedPtr<FString>(new FString("One")));
             something.Add(TSharedPtr<FString>(new FString("Two")));
             something.Add(TSharedPtr<FString>(new FString("Three")));
     
     
             HeaderRow.NameContent()
                     [
                             StructPropertyHandle->CreatePropertyNameWidget(LOCTEXT("Task", "Task Names"), LOCTEXT("IDK","IDK"), false, true, false)
                     ]
             .ValueContent()
                     .MinDesiredWidth(250)
                     [
                             SNew(STextComboBox)
                             .OptionsSource(&something)
                     ];
     }
      
     void FTaskComponentDataCustomization::CustomizeChildren(TSharedRef<class IPropertyHandle> StructPropertyHandle, class IDetailChildrenBuilder& StructBuilder, IPropertyTypeCustomizationUtils& StructCustomizationUtils)
     {
     }
      
     
     EVisibility FTaskComponentDataCustomization::GetPropertyVisibility(UProperty* InProperty) const {
             return EVisibility::Visible;
     }

I have then included this custom structure in my component subclass like this:

 

Code:

UPROPERTY(EditAnywhere, Category = "Planning | Task")
     FTaskComponentData                                                        TaskData;

I then register with the FPropertyEditorModule like so:

 

Code:

FPropertyEditorModule& PropertyModule = FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
     
             //Custom properties
             PropertyModule.RegisterCustomPropertyTypeLayout("TaskComponentData", FOnGetPropertyTypeCustomizationInstance::CreateStatic(&FTaskComponentDataCustomization::MakeInstance));

At this point, the desired combo box shows up.. I have 2 questions:

 

1) How can I set TArray so that I can update the data members with different strings? 

 

2) How do I register the property change listener? Right now, none of the property change listeners are fired from my component when I try to select values from my combobox.

 

Or where do I got to dig up any of this functionality?

 

来自 <[*https://forums.unrealengine.com/development-discussion/engine-source-github/124416-help-custom-struct-property-editor-add-setter-and-listener*](https://forums.unrealengine.com/development-discussion/engine-source-github/124416-help-custom-struct-property-editor-add-setter-and-listener)> 
