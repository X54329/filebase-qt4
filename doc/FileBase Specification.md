# FileBase Specification

> Please be aware that **FileBase** is still under heavy development and both
> it's specifications and related programs & libraries may change any time
> without backwards compatibility. Always check for updates and be careful.

**FileBase** is an XML file format to store metadata about files.

## Property-Value
In **FileBase**, every file has values for specified properties.

Using this key-value like property-value system, users can made complicated
searches like

> Find **drama** movies that is *directed* by **Stanley Kubrick**
which has **Turkish** *subtitles*.

Than programs may search for files that has "Stanley Kubrick" value fo
"Director" property and "Drama" for "Genre" and "Turkish" for "Subtitle".

* There can be multiple values for a single property, but there must be at least
one value for each property.

* All properties and values are in string type by default. (But we want to add
  type support in next versions of **FileBase**. For example, for a property
  named "Date", it's much better to have a `date` type. So, users can made
  queries like:

  > Find movies that is *directed* by **Stanley Kubrick** and *relased* between
  > **1980 and 1990**

  instead of

  > Find movies that is *directed* by **Stanley Kubrick** and *relased* in
  > **1980** or **1981** or **...** or **1989**

  for searcing Kubrick's movies that is relased between 1980-1990.)

## FileBase Example
```xml
<?xml version="1.0" encoding="UTF-8"?>

<filebase>
	<meta>
		<version>
			<major>0</major>
			<minor>0</minor>
			<patch>0</patch>
		</version>
	</meta>

	<properties>
		<property id="0">
			<name>Author</name>
		</property>
		
		<property id="1">
			<name>Genre</name>
		</property>

		<property id="2">
			<name>Year</name>
		</property>

		<property id="3">
			<name>Language</name>
		</property>
	</properties>

	<files>
		<file>
			<name>The Rubáiyát of Omar Khayyám</name>
			<path>rubaiyat.mobi</path>
			<property pid="0">Omar Khayyám</property>
			<property pid="1">Poetry</property>
			<property pid="2">1889</property>
			<property pid="3">English</property>
		</file>
		<file>
			<name>Metro 2033</name>
			<path>russian/metro2033.epub</path>
			<property pid="0">Dmitry Glukhovsky</property>
			<property pid="1">Post-apocalyptic</property>
			<property pid="1">Science Fiction</property>
			<property pid="2">2005</property>
			<property pid="3">Russian</property>
		</file>
		<file>
			<name>The Hitchhiker's Guide to the Galaxy</name>
			<path>hg2g.pdf</path>
			<property pid="0">Douglas Adams</property>
			<property pid="1">Comedy</property>
			<property pid="1">Science Fiction</property>
			<property pid="2">1979</property>
			<property pid="3">English</property>
		</file>
	</files>
</filebase>
```
### meta
```xml
	<meta>
		<version>
			<major>0</major>
			<minor>0</minor>
			<patch>0</patch>
		</version>
	</meta>
```

* `meta` tag contains information about **FileBase** itself.
* Every **FileBase** must contain `meta` tag with all of it's elements.
* `version` tag contains version of **FileBase**. For detailed information about
  versioning, please look at [Semantic Versioning](http://semver.org/).
* We suggest for programs that will use **FileBase** to check **FileBase**
  version before parsing it to prevent any errors.

> Because **FileBase** is under heavy development, so we may not change version
> until initial stable release. It's version may stay as `0.0.0` but things can
> be changed, so check the docs for latest updates.
>
> And please wait before rolling your own programs until things became stable.

### properties
```xml
	<properties>
		<property id="0">
			<name>Author</name>
		</property>
		
		<property id="1">
			<name>Genre</name>
		</property>

		<property id="2">
			<name>Year</name>
		</property>

		<property id="3">
			<name>Language</name>
		</property>
	</properties>
```
* `properties` tag contains `property`s which contains a single property.
* Every **FileBase** **must** contain `properties` tag, even if there are no
  properties.

#### property
```xml
		<property id="0">
			<name>Author</name>
		</property>
```
* All `property`s must has an `id` attribute that to be used later by
  **values**.
* `property` `id`s must start from 0 and must be sequential.

### files
```xml
	<files>
		<file>
			<name>The Rubáiyát of Omar Khayyám</name>
			<path>rubaiyat.mobi</path>
			<property pid="0">Omar Khayyám</property>
			<property pid="1">Poetry</property>
			<property pid="2">1889</property>
			<property pid="3">English</property>
		</file>
		<file>
			<name>Metro 2033</name>
			<path>russian/metro2033.epub</path>
			<property pid="0">Dmitry Glukhovsky</property>
			<property pid="1">Post-apocalyptic</property>
			<property pid="1">Science Fiction</property>
			<property pid="2">2005</property>
			<property pid="3">Russian</property>
		</file>
		<file>
			<name>The Hitchhiker's Guide to the Galaxy</name>
			<path>hg2g.pdf</path>
			<property pid="0">Douglas Adams</property>
			<property pid="1">Comedy</property>
			<property pid="1">Science Fiction</property>
			<property pid="2">1979</property>
			<property pid="3">English</property>
		</file>
	</files>
```
* `files` tag contains `file`s which contains information about files.
* Every **FileBase** **must** contain `files` tag, even if there is no files.
#### file
```xml
		<file>
			<name>The Rubáiyát of Omar Khayyám</name>
			<path>rubaiyat.mobi</path>
			<property pid="0">Omar Khayyám</property>
			<property pid="1">Poetry</property>
			<property pid="2">1889</property>
			<property pid="3">English</property>
		</file>
```
* All `file`s must has got a `name` tag, a `path` tag, and values (`property`
  tags with `pid`s) for each property.
* `name` tag contains the name of the file to be shown. For example a file could
  be named as "metro2033.epub" but it's name can be "Metro 2033".

  Generally this is useful for files that has a "title" metadata.
		  
* `path` tag contains **relative** path of file to the **FileBase**.

  In case you missed it, we are repeating: the path is **relative** to
  **FileBase**, it is **not absolute** path!

* `path` is **always** seperated using `/`. We choose that because; some
  (actually, many) POSIX systems allow `\` as a file or directory name; but
  Windows use that character as path seperator. The problem is that example is
  correct (but have different meanings under different platforms):
  ```
  aaa\\bbb\\ccc\\ddd
  ```

  Under NT, it's a path to a file named `ddd`; under POSIX, it's a file named
  "aaa\\bbb\\ccc\\ddd" and that is in the same directory with **FileBase**!
  Because of this, we can't just simply use `path.replace("\\", os.sep) under
  POSIX.

  As you can see, using `\` in file and directory names will causes a lot of
  trouble and confusion. It will also cause trouble on NT arcihtechture and NTFS
  (You should especially be careful under Linux when working with NTFS
  partitions, beacause you can create files and folders which can contain `\` at
  their name. But when you try to accsess them with Windows, you will get error.
  [For details][NTFS3G]).
		  
* `property` tags in `file` tags are also called as "values". They must have a
  `pid` (which is short abbreviation of "property id") which builds a
  relationship between *value* and *property*.

----

End of the **FileBase** Specification.

Please contact me (Bora Mert Alper <boramalper@gmail.com>) for grammatical,
techincal, and other mistakes; improvements and anything else.

[NTFS3G]: http://www.tuxera.com/community/ntfs-3g-faq/#posixfilenames2
