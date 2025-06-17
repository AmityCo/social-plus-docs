---
description: Customizing UIKit v4 with config file.
---

# Customization

In Social Plus UIKit 4.0, customization is a pivotal aspect, allowing for extensive personalization across UI elements, components, and pages. Understanding the hierarchy and role of each of these entities is crucial for effectively utilizing the UIKit's capabilities.

## <mark style="color:blue;">Understanding Elements, Components, and Pages</mark>

### **UI Elements:**

* **Definition**: The fundamental building blocks of the user interface.
* **Characteristics**: Atomic views constitute the most basic UI elements, offering essential interactivity and visual elements but often requiring additional structure to fulfill complete business use cases​​.
* **Example**: A button or an individual text field.

### **Components:**

* **Definition**: Combinations of UI elements that serve a specific function.
* **Types**: Divided into Presentational and Controller components.
  * **Presentational Components**: Direct renderers, providing straightforward rendering capabilities. They offer high flexibility and are foundational for Controller components​​.
  * **Controller Components**: Handle complex logic and are pivotal in supporting various business use cases. For example, `FeedList` or `PostView` components​​.
* **Customization**: Both types of components offer diverse customization opportunities, from visual appearance to functional behavior.

### **Pages:**

* **Definition**: Represent distinct screens within an application, offering a focused set of content and functionality.
* **Role**: A page comprises a combination of UI elements and components, providing a holistic user experience. It acts as a container for various components and elements tailored to specific user objectives​​.
* **Customization**: Pages can be tailored in terms of layout, content, and the interactivity of the components they contain.

## <mark style="color:blue;">Customization Options</mark>

### **Feature Settings:**

* **Scope**: Global level.
* **Purpose**: Configure business-specific settings.
* **Example**: Allow or restrict certain types of posts or messages​​.

### **Theme Settings:**

* **Scope**: Global level.
* **Purpose**: Define the visual appearance of UI elements uniformly.
* **Example**: Set primary and secondary colors and font family​​.

### **Element Customization:**

* **Scope**: Local level, per element.
* **Purpose**: Configure individual UI elements according to specific requirements.
* **Limitation**: This does not include customization of internal views of an element​​.

### **Internal View Customization:**

* **Scope**: Local level, specific to Controller components.
* **Purpose**: Customize internal views within Controller components.
* **Example**: Altering cells within `ConversationList` or modifying views in `PostView`​​.

## <mark style="color:blue;">Event-Driven API and Navigation Management</mark>

* **Event-Driven API**: Allows for maximum adaptability in crafting user journeys, particularly suited for simpler UI scenarios like standalone views​​.
* **UIKit Managed Navigation**: For more complex UI scenarios, such as pages, the framework autonomously manages flow, navigation, and transitions, leveraging common business logic assumptions​​.

{% content-ref url="customization-basics.md" %}
[customization-basics.md](customization-basics.md)
{% endcontent-ref %}
